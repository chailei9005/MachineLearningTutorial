#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
处理脚本的集合

Created by C.L.Wang
"""

import pyexcel

from clinic_prediction.constants import DATA_DIR, RESULT_DIR
from project_utils import *
from root_dir import ROOT_DIR


def process_words_file_180111(rf_list, wf_list, rule_file):
    """
    在分诊词表中, 小儿科添加词汇, 营养科删除一部分添加一部分.
    :param rf_list: 读取文件列表
    :param wf_list: 写入文件列表
    :param rule_file: 规则的Excel文件
    :return: 写入文件
    """
    xe_r_file = rf_list[0]
    yy_r_file = rf_list[1]
    print "小儿科读取文件: %s" % xe_r_file
    print "营养科读取文件: %s" % yy_r_file
    xe_w_file = wf_list[0]
    yy_w_file = wf_list[1]
    print "小儿科写入文件: %s" % xe_w_file
    print "营养科写入文件: %s" % yy_w_file

    # 营养科删除, 增加, 小儿科增加
    yy_remove_set, yy_add_set, xe_add_set = get_excel_data(rule_file)  # 读取Excel文件

    process_word_from_file(yy_r_file, yy_w_file, yy_remove_set, yy_add_set)  # 处理营养科文件
    process_word_from_file(xe_r_file, xe_w_file, [], xe_add_set)  # 处理小儿科文件


def process_word_from_file(r_file, w_file, remove_list, add_list):
    """
    从文件中删除或添加单词
    :param r_file: 读取文件
    :param w_file: 写入文件
    :param remove_list: 删除单词
    :param add_list: 添加单词
    :return: 写入文件
    """
    print "-" * 30 + "处理单词" + "-" * 30
    if os.path.exists(w_file):
        print "\t\t文件存在，删除文件：%s" % w_file
        os.remove(w_file)  # 删除已有文件

    print "\t\t读取文件: %s" % r_file
    print "\t\t写入文件: %s" % w_file
    data_lines = read_file(r_file)
    print "\t\t营养科词数: %s, 删除: %s, 添加: %s" % (len(data_lines), len(remove_list), len(add_list))

    res_set = set()

    for data in data_lines:  # 写入非删除文件
        if unicode(data) in remove_list:
            continue
        res_set.add(unicode(data))

    for data in add_list:  # 写入添加文件
        res_set.add(unicode(data))

    res_list = sorted(list(res_set))  # 将单词排序

    for res_data in res_list:  # 写入文件
        write_line(w_file, res_data)

    print "\t\t最终词数: %s" % (len(read_file(w_file)))
    print "-" * 67


def get_excel_data(file_name):
    """
    处理Excel数据
    :return: 策略数据
    """
    excel_data = pyexcel.load(file_name)
    lines = excel_data.get_internal_array()
    yy_remove_list = []
    yy_add_list = []
    xe_add_list = []
    for index in range(1, len(lines)):
        yingyang_remove = unicode(lines[index][0])
        yingyang_add = unicode(lines[index][1])
        xiaoer_add = unicode(lines[index][2])

        safe_add(yingyang_remove, yy_remove_list)
        safe_add(yingyang_add, yy_add_list)
        safe_add(xiaoer_add, xe_add_list)

    print "营养科-去掉: %s, 营养科-新增: %s, 儿科-新增: %s" % (len(yy_remove_list), len(yy_add_list), len(xe_add_list))

    return set(yy_remove_list), set(yy_add_list), set(xe_add_list)


def safe_add(item, item_list):
    if item:
        item_list.append(item)


def test_of_process_words_file_180111():
    """
    数据来源分诊工程的词表
    :return: 写入文件
    """
    xiaoer_file = os.path.join(ROOT_DIR, DATA_DIR, "20180111/小儿科")
    yingyang_file = os.path.join(ROOT_DIR, DATA_DIR, "20180111/营养科")

    o_xiaoer_file = os.path.join(ROOT_DIR, RESULT_DIR, "20180111/小儿科.out")
    o_yingyang_file = os.path.join(ROOT_DIR, RESULT_DIR, "20180111/营养科.out")

    rule_file = os.path.join(ROOT_DIR, DATA_DIR, "20180111/反馈.xlsx")

    process_words_file_180111([xiaoer_file, yingyang_file], [o_xiaoer_file, o_yingyang_file], rule_file)


if __name__ == '__main__':
    test_of_process_words_file_180111()  # 处理细分词
