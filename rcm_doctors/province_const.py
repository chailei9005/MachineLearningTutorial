#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
省份常量

Created by C.L.Wang
"""

from project_utils import *
from rcm_doctors.constants import DATA_DIR
from root_dir import ROOT_DIR

_PROVINCE_STD_DICT = None  # 省份简称的全局变量
_PROVINCE_CITY_DICT = None  # 省份城市的全局变量


def load_global_province_std():
    global _PROVINCE_STD_DICT
    if not _PROVINCE_STD_DICT:
        print "\t加载全局省份简称!"
        _PROVINCE_STD_DICT = load_province_std()
    return _PROVINCE_STD_DICT


def load_province_std():
    """
    加载省份名称文件
    :return: 省份简称字典
    """
    file_name = os.path.join(ROOT_DIR, DATA_DIR, 'province_std_dict')
    data_lines = read_file(file_name)
    if not data_lines:
        print "异常: 省份标准文件为空!!!"
        return {}

    res_dict = dict()
    for data_line in data_lines:
        data_list = data_line.split(',')
        if len(data_list) >= 2:
            data_list = [unicode(x) for x in data_list]
            for index in range(1, len(data_list)):
                res_dict[data_list[index]] = data_list[0]

    return res_dict


def to_province_std(prv_name):
    """
    转换为标准省份
    :param prv_name: 省份别名
    :return: 省份标准名
    """
    prv_name = unicode(prv_name)
    prv_dict = load_global_province_std()
    for prv_simple in prv_dict.keys():
        if prv_simple in prv_name:
            return prv_dict[prv_simple]
    return ''


def load_global_province_city():
    global _PROVINCE_CITY_DICT
    if not _PROVINCE_CITY_DICT:
        print "\t加载全局省份城市!"
        _PROVINCE_CITY_DICT = load_province_city()
    return _PROVINCE_CITY_DICT


def load_province_city():
    """
    加载省份核心城市文件
    :return: 省份城市字典
    """
    file_name = os.path.join(ROOT_DIR, DATA_DIR, 'province_city_dict')
    data_lines = read_file(file_name)
    if not data_lines:
        print "异常: 省份城市文件为空!!!"
        return {}
    res_dict = dict()
    for data_line in data_lines:
        data_list = data_line.split(',')
        if len(data_list) >= 2:
            data_list = [unicode(x) for x in data_list]
            res_dict[data_list[0]] = data_list[1:]  # 省份的核心城市，可能含有多个
        elif len(data_list) == 1:
            res_dict[data_list[0]] = list()  # 只有省份，则表示全部城市均可，如北京的各个区
    return res_dict


def is_big_city(prv, city):
    """
    判断省份和核心城市是否匹配
    :param prv: 省份
    :param city: 城市
    :return: 是否匹配
    """
    prv = unicode(prv)
    city = unicode(city)
    if len(city) <= 1:
        print "异常: 城市名称过短!!!"
        return False
    prv_city_dict = load_global_province_city()
    prv_std = to_province_std(prv)  # 转换为标准省份名称
    if not prv_std:
        print "异常: 非省份名称!!!"
        return False
    city_list = prv_city_dict.get(prv_std, None)  # 获取城市列表
    if not city_list:
        return True  # 未指定的均可
    for big_city in city_list:
        if city in big_city:  # 可能是简写
            return True  # 在大城市列表中
    return False  # 默认返回False


def match_province_user_and_dct(uid, did):
    """
    匹配用户和医生的省份
    :param uid: 用户ID
    :param did: 医生ID
    :return: 是否匹配
    """



def test_of_to_province_std():
    print to_province_std("新疆省")
    print to_province_std(u"甘肃")
    print to_province_std(u"吉林省")
    print to_province_std("广西省")


def test_of_match_prv_and_city():
    print is_big_city('河北', u'石家庄')
    print is_big_city(u'辽宁省', '大连')
    print is_big_city('新疆省', u'乌鲁木齐')
    print is_big_city('新疆省', u'齐齐哈尔')


if __name__ == '__main__':
    # test_of_to_province_std()  # 测试省份标准名称转换
    test_of_match_prv_and_city()
