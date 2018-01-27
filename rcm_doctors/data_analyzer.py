#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
分析数据的各个维度, 为训练数据做准备

Created by C.L.Wang
"""

from project_utils import *
from rcm_doctors.analysis_scripts import PROVINCE_SIMPLIFY
from rcm_doctors.clinic_const import ClinicUtils
from rcm_doctors.constants import DATA_DIR, RESULT_DIR
from root_dir import ROOT_DIR

# 省份列表, 33维
PROVINCE_LIST = [
    u"上海市", u"云南省", u"内蒙古自治区", u"北京市", u"吉林省",
    u"四川省", u"天津市", u"宁夏回族自治区", u"安徽省", u"山东省",
    u"山西省", u"广东省", u"广西壮族自治区", u"新疆维吾尔自治区", u"江苏省",
    u"江西省", u"河北省", u"河南省", u"浙江省", u"海南省",
    u"湖北省", u"湖南省", u"澳门特别行政区", u"甘肃省", u"福建省",
    u"西藏自治区", u"贵州省", u"辽宁省", u"重庆市", u"陕西省",
    u"青海省", u"黑龙江省", u'None'
]


def analyze_data_set(purch_file, click_file, show_file, result_file):
    """
    分析数据集中的数据维度
    92682189,clinic_web_a5769eed5c142e2b,16.3333333333,m,湖北省,460,56,172,-1,0.833333333333,
    2,12,3,9,0,1,1,4,0.33,3,
    0.75,-1,-1,30,9,20,1,3.33,26,7,
    20,1,3.71,will_to_pay,user_value,None,None,None,None,None,
    None,48.4166666667,男,副主任医师,50,山东省,二级甲等,be,1
    :param purch_file: 购买文件
    :param click_file: 点击文件
    :param show_file: 展示文件
    :param result_file: 结果文件
    :return: None
    """
    purch_lines = []
    click_lines = []
    show_lines = []
    purch_lines = read_file(purch_file)
    # click_lines = read_file(click_file)
    # show_lines = read_file(show_file)

    print "\t购买文件: %s, 行数: %s" % (purch_file, len(purch_lines))
    print "\t点击文件: %s, 行数: %s" % (click_file, len(click_lines))
    print "\t展示文件: %s, 行数: %s" % (show_file, len(show_lines))
    print "\t输出文件: %s" % result_file

    create_file(result_file)

    purch_data = purch_lines[0].split(',')
    print_and_save(result_file, "数据维度: %s" % len(purch_data))

    age_dict = collections.defaultdict(int)  # 年龄
    gender_dict = collections.defaultdict(int)  # 性别
    province_dict = collections.defaultdict(int)  # 省份
    gold_dict = collections.defaultdict(int)  # 金币数
    weight_dict = collections.defaultdict(int)  # 体重
    height_dict = collections.defaultdict(int)  # 身高
    ehr_dict = collections.defaultdict(int)  # 档案数
    join_dict = collections.defaultdict(int)  # 加入平台时间
    platform_dict = collections.defaultdict(int)  # 用户平台
    graph_total_dict = collections.defaultdict(int)  # 图文总数
    free_total_dict = collections.defaultdict(int)  # 免费图文数
    paid_total_dict = collections.defaultdict(int)  # 付费图文数
    refund_total_dict = collections.defaultdict(int)  # 图文退款数
    rebuy_total_dict = collections.defaultdict(int)  # 图文重复购买数
    revisit_total_dict = collections.defaultdict(int)  # 图文访问数
    rate_dict = collections.defaultdict(int)  # 评价数
    rate_ratio_dict = collections.defaultdict(int)  # 评价率
    good_rate_dict = collections.defaultdict(int)  # 好评数
    good_rate_ratio_dict = collections.defaultdict(int)  # 好评率
    reward_num_dict = collections.defaultdict(int)  # 打赏数
    reward_paid_dict = collections.defaultdict(int)  # 打赏金额
    reward_avg_dict = collections.defaultdict(int)  # 打赏均值 (额外)

    order_value_dict = collections.defaultdict(int)  # 订单额
    order_num_dict = collections.defaultdict(int)  # 订单数
    order_max_dict = collections.defaultdict(int)  # 订单最大
    order_min_dict = collections.defaultdict(int)  # 订单最小
    order_avg_dict = collections.defaultdict(int)  # 订单均值
    graph_value_dict = collections.defaultdict(int)  # 图文额
    graph_num_dict = collections.defaultdict(int)  # 图文数
    graph_max_dict = collections.defaultdict(int)  # 图文最大
    graph_min_dict = collections.defaultdict(int)  # 图文最小
    graph_avg_dict = collections.defaultdict(int)  # 图文均值

    tags_dict = collections.defaultdict(int)  # 标签

    d_age_dict = collections.defaultdict(int)  # 医生年龄
    d_gender_dict = collections.defaultdict(int)  # 医生性别
    d_title_dict = collections.defaultdict(int)  # 医生职称
    d_graph_dict = collections.defaultdict(int)  # 医生图文价
    d_province_dict = collections.defaultdict(int)  # 医院省份
    d_level_dict = collections.defaultdict(int)  # 医院等级
    d_clinic_dict = collections.defaultdict(int)  # 科室号

    for data_line in purch_lines:
        purch_data = data_line.split(',')
        uid = purch_data[0]  # 用户ID
        did = purch_data[1]  # 医生ID

        age_dict[process_float_field(purch_data[2])] += 1  # 用户年龄
        gender_dict[process_value_field(purch_data[3])] += 1  # 用户性别
        province_dict[process_province_field(purch_data[4])] += 1  # 用户省份
        gold_dict[process_float_field(purch_data[5])] += 1  # 金币数
        weight_dict[process_float_field(purch_data[6])] += 1  # 体重
        height_dict[process_float_field(purch_data[7])] += 1  # 身高
        ehr_dict[process_float_field(purch_data[8])] += 1  # 档案数
        join_dict[process_float_field(purch_data[9])] += 1  # 加入时间
        platform_dict[process_platform_field(purch_data[10])] += 1  # 用户平台
        graph_total_dict[process_float_field(purch_data[11])] += 1  # 图文总数
        free_total_dict[process_float_field(purch_data[12])] += 1  # 免费图文数
        paid_total_dict[process_float_field(purch_data[13])] += 1  # 付费图文数
        refund_total_dict[process_float_field(purch_data[14])] += 1  # 图文退款数
        rebuy_total_dict[process_float_field(purch_data[15])] += 1  # 图文重复购买数
        revisit_total_dict[process_float_field(purch_data[16])] += 1  # 图文重复访问数
        rate_dict[process_float_field(purch_data[17])] += 1  # 评价数
        rate_ratio_dict[process_float_field(purch_data[18])] += 1  # 评价率
        good_rate_dict[process_float_field(purch_data[19])] += 1  # 好评数
        good_rate_ratio_dict[process_float_field(purch_data[20])] += 1  # 好评率
        reward_num_dict[process_float_field(purch_data[21])] += 1  # 打赏数
        reward_paid_dict[process_float_field(purch_data[22])] += 1  # 打赏金额
        reward_avg = safe_div(process_float_field(purch_data[22]), process_float_field(purch_data[21]))  # 打赏均值 (额外)
        reward_avg_dict[reward_avg] += 1  # 打赏均值

        order_value_dict[process_float_field(purch_data[23])] += 1  # 订单额
        order_num_dict[process_float_field(purch_data[24])] += 1  # 订单数
        order_max_dict[process_float_field(purch_data[25])] += 1  # 订单最大
        order_min_dict[process_float_field(purch_data[26])] += 1  # 订单最小
        order_avg_dict[process_float_field(purch_data[27])] += 1  # 订单均值
        graph_value_dict[process_float_field(purch_data[28])] += 1  # 图文额
        graph_num_dict[process_float_field(purch_data[29])] += 1  # 图文数
        graph_max_dict[process_float_field(purch_data[30])] += 1  # 图文最大
        graph_min_dict[process_float_field(purch_data[31])] += 1  # 图文最小
        graph_avg_dict[process_float_field(purch_data[32])] += 1  # 图文均值

        tags_dict = process_tags_fields(purch_data[33:41], tags_dict)  # 标签列, 8维

        d_age_dict[process_float_field(purch_data[41])] += 1  # 医生年龄
        d_gender_dict[process_value_field(purch_data[42])] += 1  # 医生性别
        d_title_dict[process_value_field(purch_data[43])] += 1  # 医生职称
        d_graph_dict[process_float_field(purch_data[44])] += 1  # 医生图文价格
        d_province_dict[process_province_field(purch_data[45])] += 1  # 医生省份
        d_level_dict[process_value_field(purch_data[46])] += 1  # 医院等级
        d_clinic_dict[process_clinic_field(purch_data[47])] += 1  # 医生科室

    print_and_save(result_file, "第1维年龄:[%s, %s, %s]" % (analyze_continuous_dict(age_dict)))
    print_and_save(result_file, "第2维性别:维度:%s, 数据:%s" % (analyze_cate_dict(gender_dict), get_dict_str(gender_dict)))
    print_and_save(result_file, "第3维省份:维度:%s, 数据:%s" % (analyze_cate_dict(province_dict), get_dict_str(province_dict)))
    print_and_save(result_file, "第4维金币数:[%s, %s, %s]" % (analyze_continuous_dict(gold_dict)))
    print_and_save(result_file, "第5维体重:[%s, %s, %s]" % (analyze_continuous_dict(weight_dict)))
    print_and_save(result_file, "第6维身高:[%s, %s, %s]" % (analyze_continuous_dict(height_dict)))
    print_and_save(result_file, "第7维档案数:[%s, %s, %s]" % (analyze_continuous_dict(ehr_dict)))  # 无效
    print_and_save(result_file, "第8维加入时间:[%s, %s, %s]" % (analyze_continuous_dict(join_dict, False)))  # 无异常值
    print_and_save(result_file, "第9维平台:维度:%s, 数据:%s" % (analyze_cate_dict(platform_dict), get_dict_str(platform_dict)))
    print_and_save(result_file, "第10维图文总数:[%s, %s, %s]" % (analyze_continuous_dict(graph_total_dict)))
    print_and_save(result_file, "第11维免费图文数:[%s, %s, %s]" % (analyze_continuous_dict(free_total_dict)))
    print_and_save(result_file, "第12维付费图文数:[%s, %s, %s]" % (analyze_continuous_dict(paid_total_dict)))
    print_and_save(result_file, "第13维图文退款数:[%s, %s, %s]" % (analyze_continuous_dict(refund_total_dict)))
    print_and_save(result_file, "第14维图文重复购买数:[%s, %s, %s]" % (analyze_continuous_dict(rebuy_total_dict)))
    print_and_save(result_file, "第15维图文重复访问数:[%s, %s, %s]" % (analyze_continuous_dict(revisit_total_dict)))
    print_and_save(result_file, "第16维评价数:[%s, %s, %s]" % (analyze_continuous_dict(rate_dict)))
    print_and_save(result_file, "第17维评价率:[%s, %s, %s]" % (analyze_continuous_dict(rate_ratio_dict, False)))  # 无异常值
    print_and_save(result_file, "第18维好评数:[%s, %s, %s]" % (analyze_continuous_dict(good_rate_dict)))
    print_and_save(result_file, "第19维好评率:[%s, %s, %s]" % (analyze_continuous_dict(good_rate_ratio_dict, False)))  # 无异常值
    print_and_save(result_file, "第20维打赏数:[%s, %s, %s]" % (analyze_continuous_dict(reward_num_dict)))
    print_and_save(result_file, "第21维打赏金额:[%s, %s, %s]" % (analyze_continuous_dict(reward_paid_dict)))
    print_and_save(result_file, "第22维打赏均值:[%s, %s, %s]" % (analyze_continuous_dict(reward_avg_dict)))  # 额外

    print_and_save(result_file, "第23维订单额:[%s, %s, %s]" % (analyze_continuous_dict(order_value_dict)))
    print_and_save(result_file, "第24维订单数:[%s, %s, %s]" % (analyze_continuous_dict(order_num_dict)))
    print_and_save(result_file, "第25维订单最大:[%s, %s, %s]" % (analyze_continuous_dict(order_max_dict)))
    print_and_save(result_file, "第26维订单最小:[%s, %s, %s]" % (analyze_continuous_dict(order_min_dict)))
    print_and_save(result_file, "第27维订单均值:[%s, %s, %s]" % (analyze_continuous_dict(order_avg_dict)))
    print_and_save(result_file, "第28维图文额:[%s, %s, %s]" % (analyze_continuous_dict(graph_value_dict)))
    print_and_save(result_file, "第29维图文数:[%s, %s, %s]" % (analyze_continuous_dict(graph_num_dict)))
    print_and_save(result_file, "第30维图文最大:[%s, %s, %s]" % (analyze_continuous_dict(graph_max_dict)))
    print_and_save(result_file, "第31维图文最小:[%s, %s, %s]" % (analyze_continuous_dict(graph_min_dict)))
    print_and_save(result_file, "第32维图文均值:[%s, %s, %s]" % (analyze_continuous_dict(graph_avg_dict)))

    tags_dict = analyze_tags_dict(tags_dict)  # 省略频次较低的标签, 保留30维
    print_and_save(result_file, "第33维标签列表:维度:%s, 数据:%s" % (analyze_cate_dict(tags_dict), get_dict_str(tags_dict)))

    print_and_save(result_file, "第34维医生年龄:[%s, %s, %s]" % (analyze_continuous_dict(d_age_dict)))
    print_and_save(result_file,
                   "第35维医生性别:维度:%s, 数据:%s" % (analyze_cate_dict(d_gender_dict), get_dict_str(d_gender_dict)))
    print_and_save(result_file, "第36维医生职称:维度:%s, 数据:%s" % (analyze_cate_dict(d_title_dict), get_dict_str(d_title_dict)))
    print_and_save(result_file, "第37维医生图文价格:[%s, %s, %s]" % (analyze_continuous_dict(d_graph_dict)))
    print_and_save(result_file,
                   "第38维医生省份:维度:%s, 数据:%s" % (analyze_cate_dict(d_province_dict), get_dict_str(d_province_dict)))

    d_level_dict = analyze_levels_dict(d_level_dict)  # 去除低频等级
    print_and_save(result_file,
                   "第39维医院等级:维度:%s, 数据:%s" % (analyze_cate_dict(d_level_dict), get_dict_str(d_level_dict)))

    print_and_save(result_file,
                   "第40维医院等级:维度:%s, 数据:%s" % (analyze_cate_dict(d_clinic_dict), get_dict_str(d_clinic_dict)))


def get_dict_str(data_dict):
    return "数据:%s\n关键字:%s" % (list_2_utf8(sort_dict_by_value(data_dict)), list_2_utf8(data_dict.keys()))


def print_and_save(file_name, out_str):
    print "\t%s" % out_str
    write_line(file_name, out_str)


def process_clinic_field(data):
    if data:
        clinic_no = ClinicUtils.clinic_no_to_online(data)
        clinic_no = ClinicUtils.clinic_no_to_rough(clinic_no)
        clinic_name = ClinicUtils.clinic_no_to_name(clinic_no)
        if clinic_name:
            return clinic_name
        else:
            return 'None'
    else:
        return 'None'


def process_tags_fields(data_list, res_dict):
    """
    处理8维标签
    :param data_list: 标签列表
    :param res_dict: 字典
    :return: 标签字典
    """
    for tag in data_list:
        if tag != 'None':
            res_dict[tag] += 1

    return res_dict


def process_platform_field(data):
    """
    处理平台的域
    :param data: 
    :return: 
    """
    if data == '-1':  # -1的平台和0的平台统一为0, 0的数据较少, 购买中就两个
        return '0'
    else:
        return data


def process_province_field(data):
    """
    处理省份数据的逻辑
    :param data: 省份
    :return: 处理后的省份
    """
    if data:
        data = unicode(data).strip()
        if data in PROVINCE_SIMPLIFY:  # 处理省份简写
            data = PROVINCE_SIMPLIFY[data]
        return data
    else:
        return 'None'


def process_value_field(data):
    """
    默认处理数据样式
    :param data: 旧数据
    :return: 新数据
    """
    if data:
        return data
    else:
        return 'None'


def process_float_field(data):
    """
    处理数字型数据
    :param data: 旧数据 
    :return: 新数据
    """
    if data:
        try:
            value = float(data)
            if value >= 0.0:
                return value
            else:
                return 0.0
        except Exception as e:
            return 0.0
    else:
        return 0.0


def analyze_tags_dict(tags_dict):
    """
    标签只保留最常用的30维
    
    ["chinese_medical_test", "baby_cough", "will_to_pay", "downs_screening", "baby_expectorant", 
    "hypertension", "depression", "skin_care", "user_value", "emotional_guidance", 
    "breast_milk", "impotence", "mental_impotence", "alopecia", "gastroscope_colonoscope",
     "physical_examination", "heart_disease", "baby_growth", "parenting", "diet", 
     "baby_allergies", "breast_diseases", "will_to_reward_doctor", "gynaecology", "pregnant", 
     "baby_diarrhea", "anxious", "inferiority", "headache", "good_rating"]

    :param tags_dict: 
    :return: 
    """
    res_dict = collections.defaultdict(int)
    for tag in tags_dict.keys():
        if tags_dict[tag] >= 4900:  # 去掉小众标签
            res_dict[tag] = tags_dict[tag]
    print "\t\t标签列表: %s" % list_2_utf8(res_dict.keys())
    return res_dict


def analyze_levels_dict(d_level_dict):
    res_dict = collections.defaultdict(int)
    for tag in d_level_dict.keys():
        if d_level_dict[tag] >= 800:  # 去掉小众标签
            res_dict[tag] = d_level_dict[tag]
        else:
            res_dict['其他'] += d_level_dict[tag]
    print "\t\t标签列表: %s" % list_2_utf8(res_dict.keys())
    return res_dict


def analyze_cate_dict(cate_dict):
    """
    分析离散字典
    :param cate_dict: 离散字典
    :return: key的长度
    """
    cate_keys = cate_dict.keys()
    return len(sorted(cate_keys))


def analyze_continuous_dict(cnt_dict, outlier=True):
    """
    分析连续字典
    :param cnt_dict: 连续Key的字典
    :param outlier: 是否存在异常值
    :return: 最小值, 最大值
    """
    cnt_keys = cnt_dict.keys()
    sort_list = sorted(cnt_keys)
    print "\t\t连续Keys: %s" % list_2_utf8(sort_list)
    if outlier:
        last_index = int(len(sort_list) * 0.85)
    else:
        last_index = len(sort_list) - 1
    return sort_list[0], sort_list[last_index], sort_list[len(sort_list) - 1]


def test_of_analyze_data_set():
    purch_file = os.path.join(ROOT_DIR, DATA_DIR, 'train_purchase_20170101_20171120')
    click_file = os.path.join(ROOT_DIR, DATA_DIR, 'train_click_20170101_20171120')
    show_file = os.path.join(ROOT_DIR, DATA_DIR, 'train_show_20170101_20171120')
    result_file = os.path.join(ROOT_DIR, RESULT_DIR, 'train_analyzed_result')

    analyze_data_set(purch_file=purch_file, click_file=click_file, show_file=show_file, result_file=result_file)


if __name__ == '__main__':
    test_of_analyze_data_set()
