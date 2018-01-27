#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
分析著名医院的脚本

Created by C.L.Wang
"""
from django.db import connections

from project_utils import *
from rcm_doctors.constants import DATA_DIR
from root_dir import ROOT_DIR

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "configs.settings")


def save_famous_hospitals_from_mysql(out_file):
    """
    存储著名医院的名称
    :param out_file: 写入文件
    :return: None
    """
    create_file(out_file)
    cursor = connections['core_db'].cursor()
    sql = "select norm_name,is_deleted from symptomchecker_goodhospital"
    cursor.execute(sql)
    rows = cursor.fetchall()
    hsp_set = set()
    for row in rows:
        if row[1] == 0:
            hsp_set.add(unicode(row[0]))
    hsp_list = sorted(list(hsp_set))
    for hsp in hsp_list:
        write_line(out_file, hsp)


def load_famous_hospitals_from_solr(file_name):
    """
    加载solr数据源的医院
    :param file_name: 文件名
    :return: 医院集合
    """
    data_lines = read_file(file_name)
    res_set = set()
    for data_line in data_lines:
        data_list = data_line.split('\t')
        data_value = unicode(data_list[0])

        hsp_list = parse_hsp_value(data_value)
        for hsp in hsp_list:
            res_set.add(hsp)
    return res_set


def parse_hsp_value(data_value):
    """
    医院含有大量的重名现象
    :param data_value: 医院的值
    :return: 医院列表
    """
    res_list = list()
    hsp_list = data_value.split(u'/')
    for hsp_data in hsp_list:
        res_list += hsp_data.split(u'；')
    return res_list


def load_famous_hospitals_from_mysql(file_name):
    """
    加载从MySQL存储的数据
    :param file_name: 文件名
    :return: 著名医院列表
    """
    data_lines = read_file(file_name)
    res_set = set()
    for data_line in data_lines:
        res_set.add(unicode(data_line))
    return res_set


def diff_famous_hsp():
    """
    最终，数据源使用MySQL的简写著名医院，使用Solr的fq过滤选择合适的医生。
    本方法暂时并未使用
    :return: None
    """
    solr_file = os.path.join(ROOT_DIR, DATA_DIR, 'weightedstr.txt')
    solr_set = load_famous_hospitals_from_solr(solr_file)
    mysql_file = os.path.join(ROOT_DIR, DATA_DIR, 'famous_hospitals_from_mysql')
    mysql_set = load_famous_hospitals_from_mysql(mysql_file)
    mysql_list = list(mysql_set)

    res_diff = list()
    for mysql_item in mysql_list:
        is_inside = False
        for solr_item in solr_set:
            if mysql_item in solr_item:
                is_inside = True
                break
            if solr_item in mysql_item:
                is_inside = True
                break
        if not is_inside:
            res_diff.append(mysql_item)

    print list_2_utf8(list(res_diff))


def test_of_load_famous_hospitals_from_solr():
    file_name = os.path.join(ROOT_DIR, DATA_DIR, 'weightedstr.txt')
    hsp_set = load_famous_hospitals_from_solr(file_name)
    print list_2_utf8(list(hsp_set))


def test_of_save_famous_doctors_from_mysql():
    out_file = os.path.join(ROOT_DIR, DATA_DIR, 'famous_hospitals_from_mysql')
    save_famous_hospitals_from_mysql(out_file)


def test_of_load_famous_hospitals_from_mysql():
    file_name = os.path.join(ROOT_DIR, DATA_DIR, 'famous_hospitals_from_mysql')
    hsp_set = load_famous_hospitals_from_mysql(file_name)
    print list_2_utf8(list(hsp_set))


if __name__ == '__main__':
    # test_of_save_famous_doctors_from_mysql()  # 存储著名医生文件
    # test_of_load_famous_hospitals_from_solr()  # 加载Solr医生文件
    # test_of_load_famous_hospitals_from_mysql()  # 加载MySQL医生文件
    diff_famous_hsp()
