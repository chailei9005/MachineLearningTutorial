#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试HBase

Created by C.L.Wang
"""

import happybase

from configs.configs import HBaseConf
from project_utils import *


def get_problems_info_from_hbase(problem_id_list):
    """
    在HBase的问题表中，获取信息
    :param problem_id_list: 问题ID列表
    :return: 问题信息列表
    """
    row_keys = list()
    for problem_id in problem_id_list:
        row_keys.append(problem_id + "||gf")

    connection = happybase.Connection(host=HBaseConf.hbase_host, port=HBaseConf.hbase_port)
    rows = connection.table(HBaseConf.cy_service_table).rows(row_keys)

    result_dict = dict()

    for _, row_data in rows:
        pid = row_data.get('info:id', None)  # 获取ID
        print "问题ID: %s" % pid

        create_time = row_data.get('info:created_time', None)  # 创建时间 created_time - create_time
        create_time_stp = parse_time(create_time)  # 时间戳
        print "时间戳: %s" % create_time_stp

        checkups = list()  # 检查
        d_checkup = row_data.get('profile:d_checkup', None)
        checkups += parse_items(d_checkup)
        u_checkup = row_data.get('profile:u_checkup', None)
        checkups += parse_items(u_checkup)
        uf_checkup = row_data.get('profile:uf_checkup', None)
        checkups += parse_items(uf_checkup)
        print "检查: %s" % list_2_utf8(checkups)

        drugs = list()
        d_drug = row_data.get('profile:d_drug', None)
        drugs += parse_items(d_drug)
        u_drug = row_data.get('profile:u_drug', None)
        drugs += parse_items(u_drug)
        uf_drug = row_data.get('profile:uf_drug', None)
        drugs += parse_items(uf_drug)
        print "疾病: %s" % list_2_utf8(drugs)

        dc_diseases = list()
        dc_disease = row_data.get('profile:dc_disease', None)
        dc_diseases += parse_items(dc_disease)
        print "医生确诊疾病: %s" % list_2_utf8(dc_diseases)

        content_profile = json.loads(row_data.get('profile:content_info', {}))
        interaction = content_profile.get('interaction_num', 0)
        print "交互次数: %s" % interaction

        tags_result = list()
        if checkups:
            tags_result.append(u'检查建议')
        if dc_diseases:
            tags_result.append(u'可能疾病')
        if drugs:
            tags_result.append(u'用药指导')

        problem_info = [tags_result, create_time_stp, interaction]  # 转换时间
        result_dict[pid] = problem_info

        print result_dict  # 结果字典


def parse_time(create_time):
    datetime_object = datetime.strptime(create_time, '%Y-%m-%d %H:%M:%S')
    return int(datetime_object.strftime('%s')) * 1000


def parse_items(items_str):
    if not items_str:
        return []
    return items_str.split("|||")


def test_of_get_problems_info_from_hbase():
    problem_id_list = ['387512705', '147021739', '262018828', u'484993454']
    print get_problems_info_from_hbase(problem_id_list)


if __name__ == '__main__':
    test_of_get_problems_info_from_hbase()
