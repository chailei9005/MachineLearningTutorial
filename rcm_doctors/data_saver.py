#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by C.L.Wang
# 设置存储训练数据
import json
import os
import sys

reload(sys)  # 重置系统参数
sys.setdefaultencoding('utf8')  # 避免编码错误

import time
from datetime import timedelta

import happybase

from configs.hbase_configs import HBaseConf
from project_utils import write_line
from rcm_doctors.constants import DATA_DIR
from remote_access.remote_apis import get_user_features, get_doctor_features
from root_dir import ROOT_DIR

"""
购买数据: 13,4012
点击数据: 146,2623
展示数据: 1113,8352
"""


def save_train_data(start_date, end_date, log=False):
    """
    准备训练数据, 起始日期, 结束日期
    :param start_date: 起始日期
    :param end_date: 结束日期
    :param log: 是否显示日志
    :return: 写入训练数据
    """
    print "准备训练数据中... 起始: %s, 结束: %s" % (start_date, end_date)
    s_time = time.time()

    print "\t准备搜索数据(HBase)和好医院数据(MySQL), 日期: %s - %s" % (start_date, end_date)
    connection = happybase.Connection(host=HBaseConf.hbase_host, port=HBaseConf.hbase_port)
    rows = connection.table(HBaseConf.search_log_table).scan(row_start=start_date, row_stop=end_date)
    print "\t准备搜索数据(HBase)和好医院数据(MySQL)完成! "

    show_inst_set = set()  # 展示集合
    click_inst_set = set()  # 点击集合
    purch_inst_set = set()  # 购买集合

    show_path = os.path.join(ROOT_DIR, DATA_DIR, "train_show_%s_%s" % (start_date, end_date))
    if os.path.exists(show_path):
        print "\t\t文件存在，删除文件：%s" % show_path
        os.remove(show_path)  # 删除已有文件
    click_path = os.path.join(ROOT_DIR, DATA_DIR, "train_click_%s_%s" % (start_date, end_date))
    if os.path.exists(click_path):
        print "\t\t文件存在，删除文件：%s" % click_path
        os.remove(click_path)  # 删除已有文件
    purch_path = os.path.join(ROOT_DIR, DATA_DIR, "train_purchase_%s_%s" % (start_date, end_date))
    if os.path.exists(purch_path):
        print "\t\t文件存在，删除文件：%s" % purch_path
        os.remove(purch_path)  # 删除已有文件

    count = 0
    r_count = 0
    for row_key, row_data in rows:
        count += 1
        if count % 100000 == 0 or count == 1:
            print "\t\tcount %s" % count

        uid = row_data.get("info:search_uid")  # 用户ID
        if not uid:  # 没有ID直接返回
            continue

        show_did_list = []
        click_did_list = []
        purch_did_list = []

        search_result = json.loads(row_data.get("info:search_result", None))  # 搜索结果
        for search_item in search_result:
            show_did_list.append(search_item.get('id', None))  # 用户展示的ID数
        if len(show_did_list) >= 5:  # 展示取前5个
            show_did_list = show_did_list[0:5]

        for key, value in row_data.items():
            if "doctor_home_click_" in key:  # 医生点击ID
                click_did_list.append(key.replace("info:doctor_home_click_", ""))  # 点击医生列表
            if "purchase_" in key:  # 医生购买ID
                purch_did_list.append(key.replace("info:purchase_", ""))  # 购买医生列表

        show_did_list = list(set(show_did_list) - set(click_did_list) - set(purch_did_list))  # 搜索未处理的ID列表
        click_did_list = list(set(click_did_list) - set(purch_did_list))  # 点击未购买的ID列表

        if log:
            print "uid: %s, 搜索: %s, 点击: %s, 购买: %s" % (
                uid, len(show_did_list), len(click_did_list), len(purch_did_list))

        for purch_item in purch_did_list:  # 购买集合
            purch_inst_set.add((uid, purch_item))
            write_features(purch_path, uid, purch_item, True)

        for click_item in click_did_list:  # 点击集合
            click_inst_set.add((uid, click_item))
            write_features(click_path, uid, click_item, True)

        for show_item in show_did_list:  # 展示集合
            show_inst_set.add((uid, show_item))
            write_features(show_path, uid, show_item, False)

        r_count += 1
        if r_count % 10000 == 0 or r_count == 1:
            print "\t\tr_count %s" % r_count
            print "\t\t购买数: %s, 点击数: %s, 展示数: %s" % (len(purch_inst_set), len(click_inst_set), len(show_inst_set))

    print "\t总行数: %s, 目标行数: %s" % (count, r_count)
    print "\t购买数: %s, 点击数: %s, 展示数: %s" % (len(purch_inst_set), len(click_inst_set), len(show_inst_set))

    connection.close()
    print "准备训练数据完成! 耗时: %s" % timedelta(seconds=(time.time() - s_time))


def write_features(file_path, uid, did, is_pos):
    user_info_list = get_user_features(uid=uid)
    doctor_info_list = get_doctor_features(did=did)
    if not user_info_list:
        print "空用户ID: %s" % uid
        return
    if not doctor_info_list:
        print "空医生ID: %s" % did
        return
    user_info_list = [None if v is u'' else v for v in user_info_list]
    doctor_info_list = [None if v is u'' else v for v in doctor_info_list]
    line_list = [uid, did] + user_info_list + doctor_info_list
    # print line_list
    line = u','.join([unicode(str(item)) for item in line_list])
    if is_pos:
        line = line + u',1'
    else:
        line = line + u',0'
    write_line(file_path, line)  # 正例的标签是1


def test_of_save_train_data():
    """
    测试存储训练数据
    
    :return: 写入文件
    """
    save_train_data("20170101", "20171120")


if __name__ == '__main__':
    test_of_save_train_data()
