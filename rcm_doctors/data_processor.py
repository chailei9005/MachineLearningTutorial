#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
将数据集处理成特征, 根据分析结果

Created by C.L.Wang
"""

from project_utils import *
from rcm_doctors.analysis_scripts import PROVINCE_SIMPLIFY
from rcm_doctors.constants import DATA_DIR
from root_dir import ROOT_DIR


def process_data_file(file_name):
    print "\t输入文件: %s" % file_name
    out_file = file_name + ".prc"
    if os.path.exists(out_file):
        print "文件存在，删除文件：%s" % out_file
        os.remove(out_file)  # 删除已有文件
    print "\t输出文件: %s" % out_file

    data_lines = read_file(file_name)
    print "\t文件行数: %s" % len(data_lines)

    for data_line in data_lines:
        data_list = data_line.split(',')
        feature_list = parse_line(data_list)
        print "特征维度: %s, 数据: %s" % (len(feature_list), feature_list)
        break


class DataConst(object):
    MAX_LIST = {
        2: 55.0,  # 年龄, 2
        5: 7000.0,  # 金币数, 5
        6: 120.0,  # 体重, 6
        7: 180.0,  # 身高, 7
        9: 6.0,  # 加入时间, 9
        11: 700.0,  # 图文总数, 11
        12: 600.0,  # 免费图文, 12
        13: 300.0,  # 付费图文, 13
        14: 20.0,  # 图文退款, 14
        15: 160.0,  # 重复购买, 15
        16: 350.0,  # 重复访问, 16
        17: 500.0,  # 评价数, 17
        18: 1.0,  # 评价率, 18
        19: 40.0,  # 好评数, 19
        20: 1.0,  # 好评率, 20
        21: 80.0,  # 打赏数, 21
        22: 600.0,  # 打赏金额, 22
        23: 3000.0,  # 订单额
        24: 350.0,  # 订单数
        25: 900.0,  # 订单最大
        26: 70.0,  # 订单最小
        27: 100.0,  # 订单均值
        28: 1800.0,  # 图文额
        29: 250.0,  # 图文数
        30: 160.0,  # 图文最大
        31: 80.0,  # 图文最小
        32: 50.0,  # 图文均值
        41: 60.0,  # 医生年龄
        44: 120.0,  # 图文价格
    }  # 最大值

    GENDER_INDEXES = [3, 42]  # 用户性别和医生性别
    GENDER_DICT = {u"u": u'b', u"女": u'f', u"男": u'm'}
    GENDER_LIST = [u"b", u"m", u"f"]  # 第2维, 性别, 4维

    PROVINCE_INDEXES = [4, 45]  # 用户省份和医院省份
    PROVINCE_LIST = [
        u"上海市", u"云南省", u"内蒙古自治区", u"北京市", u"吉林省",
        u"四川省", u"天津市", u"宁夏回族自治区", u"安徽省", u"山东省",
        u"山西省", u"广东省", u"广西壮族自治区", u"新疆维吾尔自治区", u"江苏省",
        u"江西省", u"河北省", u"河南省", u"浙江省", u"海南省",
        u"湖北省", u"湖南省", u"澳门特别行政区", u"甘肃省", u"福建省",
        u"西藏自治区", u"贵州省", u"辽宁省", u"重庆市", u"陕西省",
        u"青海省", u"黑龙江省"]  # 第3维, 省份, 33维

    PLATFORM_INDEXES = [10]
    PLATFORM_LIST = [u"1", u"0", u"2"]  # 第9维, 平台, 3维

    TAG_START_INDEX = 33  # 维度[33:41)
    TAG_LIST = [
        u"chinese_medical_test", u"baby_cough", u"will_to_pay", u"downs_screening", u"baby_expectorant",
        u"hypertension", u"depression", u"skin_care", u"user_value", u"emotional_guidance",
        u"breast_milk", u"impotence", u"mental_impotence", u"alopecia", u"gastroscope_colonoscope",
        u"physical_examination", u"heart_disease", u"baby_growth", u"parenting", u"diet",
        u"baby_allergies", u"breast_diseases", u"will_to_reward_doctor", u"gynaecology", u"pregnant",
        u"baby_diarrhea", u"anxious", u"inferiority", u"headache", u"good_rating"
    ]

    TITLE_INDEXES = [43]
    TITLE_LIST = [u"副主任医师", u"主治医师", u"心理咨询师", u"医师", u"主任医师", u"公共营养师"]

    LEVEL_INDEXES = [46]
    LEVEL_LIST = [u"三级乙等", u"二级乙等", u"二级甲等", u"二级丙等", u"三级甲等",
                  u"一级甲等", u"三级丙等", u"协会"]

    CLINIC_INDEXES = [47]
    CLINIC_LIST = [
        u"肛肠科", u"甲状腺乳腺外科", u"骨伤科", u"妇科", u"眼科",
        u"报告解读科", u"口腔颌面科", u"儿科", u"中医科", u"消化内科",
        u"男科", u"精神心理科", u"呼吸内科", u"皮肤科", u"神经内科",
        u"心血管内科"]


def parse_line(data_list):
    """
    处理行
    :param data_list: 数据列表
    :return: 特征列表
    """
    print "\t维度: %s, 原始数据: %s" % (len(data_list), list_2_utf8(data_list))
    feature_list = []
    for index in range(len(data_list)):
        if index in DataConst.MAX_LIST.keys():
            data_value = float(data_list[index])
            if data_value < 0:  # 去除负数
                data_value = 0
            max_value = DataConst.MAX_LIST[index]
            feature_list.append(safe_div(data_value, max_value))  # 归一化
        elif index in DataConst.GENDER_INDEXES:  # 性别
            feature_list += parse_gender_for_oh(unicode(data_list[index]))
        elif index in DataConst.PROVINCE_INDEXES:  # 省份
            feature_list += parse_province_for_oh(unicode(data_list[index]))
        elif index in DataConst.PLATFORM_INDEXES:  # 平台
            feature_list += parse_dict_for_oh(unicode(data_list[index]), DataConst.PLATFORM_LIST)
        elif index == DataConst.TAG_START_INDEX:  # 标签
            feature_list += parse_list_dict_for_oh(
                data_list[DataConst.TAG_START_INDEX:DataConst.TAG_START_INDEX + 8], DataConst.TAG_LIST)
        elif index in DataConst.TITLE_INDEXES:  # 职称
            feature_list += parse_dict_for_oh(unicode(data_list[index]), DataConst.TITLE_LIST)
        elif index in DataConst.LEVEL_INDEXES:  # 医院等级
            feature_list += parse_dict_for_oh(unicode(data_list[index]), DataConst.LEVEL_LIST)
        elif index in DataConst.CLINIC_INDEXES:  # 科室
            feature_list += parse_dict_for_oh(unicode(data_list[index]), DataConst.CLINIC_LIST)
        else:
            print "\t空索引: %s" % index
    return feature_list


def parse_gender_for_oh(data):
    """
    处理性别维度
    :param data: 值
    :return: 性别的oh
    """
    res_list = list()
    if data:
        data = unicode(data).strip()
        if data in DataConst.GENDER_DICT.keys():
            data = DataConst.GENDER_DICT.get(data, None)
        for gender in DataConst.GENDER_LIST:
            if data == gender:
                res_list.append(1)
            else:
                res_list.append(0)
    else:
        for gender in DataConst.GENDER_LIST:
            res_list.append(0)
        print "\t\tException - Value: %s" % data
    print "\t\t性别oh: %s, 维度: %s" % (res_list, len(res_list))
    return res_list


def parse_province_for_oh(data):
    """
    处理省份维度
    :param data: 值
    :return: 省份的oh
    """
    res_list = list()
    if data:
        data = unicode(data).strip()
        if data in PROVINCE_SIMPLIFY.keys():  # 处理省份简写
            data = PROVINCE_SIMPLIFY.get(data, None)
        for province in DataConst.PROVINCE_LIST:
            if data == province:
                res_list.append(1)
            else:
                res_list.append(0)
    else:
        for province in DataConst.PROVINCE_LIST:
            res_list.append(0)
        print "\t\tException - Value: %s" % data
    print "\t\t省份oh: %s, 维度: %s" % (res_list, len(res_list))
    return res_list


def parse_dict_for_oh(data, std_list):
    res_list = list()
    if data:
        data = unicode(data).strip()
        for r_data in std_list:
            if data == r_data:
                res_list.append(1)
            else:
                res_list.append(0)
    else:
        for r_data in std_list:
            res_list.append(0)
        print "\t\tException - Value: %s" % data
    print "\t\toh: %s, 维度: %s" % (res_list, len(res_list))
    return res_list


def parse_list_dict_for_oh(data_list, std_list):
    res_list = list()
    data_list = [unicode(x) for x in data_list]
    for s_data in std_list:
        if s_data in data_list:
            res_list.append(1)
        else:
            res_list.append(0)
    print "\t\toh: %s, 维度: %s" % (res_list, len(res_list))
    return res_list


def test_of_process_data_file():
    purch_file = os.path.join(ROOT_DIR, DATA_DIR, 'train_purchase_20170101_20171120')
    process_data_file(file_name=purch_file)


if __name__ == '__main__':
    test_of_process_data_file()
