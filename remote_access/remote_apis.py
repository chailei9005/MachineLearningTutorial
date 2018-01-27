#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by C.L.Wang

import json
import time
from datetime import timedelta

from project_utils import get_person_age, list_2_utf8
from remote_access.services.remote_services import get_user_profile_service, get_search_service


def get_users_province(uids):
    params = {'user_ids': uids, 'fields': ['province']}
    client = get_user_profile_service()
    result = client.getUserProfileInfo(json.dumps(params))
    uid_province_dict = dict()
    for uid in uids:
        p_info = result.get(uid, None)
        if p_info:
            province = p_info.get('province', None)
            uid_province_dict[uid] = unicode(province)
        else:
            uid_province_dict[uid] = None
    return result


def get_user_features(uid, log=False):
    """
    获取用户特征, [年龄, 性别, 省份, 平台, 总额, 总单数, 最大额, 平均额]
    :param uid: 用户ID
    :param log: 是否输出日志
    :return: 用户特征
    """
    if log:
        print "提取用户特征中... uid: %s" % uid
    s_time = time.time()
    try:
        params = {'user_ids': [uid],
                  'fields':
                      ['sex', 'born_date', 'province', 'gold_coin', 'weight',
                       'height', 'ehr_num', 'join_date', 'platform', 'paid_details',
                       'graph_total_num', 'graph_free_num', 'graph_paid_num', 'graph_refund_num',
                       'graph_rebuy_num', 'graph_revisit_num', 'graph_assess_rating_num',
                       'graph_assess_rating_ratio', 'graph_assess_good_rating_num', 'graph_assess_good_rating_ratio',
                       'reward_total_num', 'reward_total_pay', 'tag_details']}
        rpc_time = time.time()  # 统计RPC时间
        client = get_user_profile_service()
        result = client.getUserProfileInfo(json.dumps(params))

        uid_info = json.loads(result)[uid]
        user_info_list = get_user_info_from_rpc_info(uid_info)  # 获取个人信息
        user_info_list = [None if v is u'' else v for v in user_info_list]
        if log:
            print u'\t年龄: %s, 性别: %s, 省份: %s, 金币数: %s, 体重: %s, ' \
                  u'身高: %s, 档案数: %s, 加入时间: %s, 用户平台: %s, 图文总数: %s, ' \
                  u'免费图文数: %s, 付费图文数: %s, 图文退款数: %s, 图文重复购买数: %s, 图文重复访问数: %s, ' \
                  u'图文评价数: %s, 图文评价率: %s, 图文好评数: %s, 图片好评率: %s, 打赏总数: %s, ' \
                  u'打赏总金额: %s' % tuple(user_info_list)

        paid_details = uid_info.get('paid_details', None)
        user_order_list = get_user_order_from_rpc_info(paid_details)  # 获取订单信息
        if log:
            print u'\t订单额: %s, 订单数: %s, 订单最大值: %s, 订单最小值: %s, 订单均值: %s, ' \
                  u'图文订单额: %s, 图文订单数: %s, 图文订单最大值: %s, 图文订单最小值: %s, 图文订单均值: %s' \
                  % tuple(user_order_list)

        tag_details = uid_info.get('tag_details', None)
        user_tag_list = get_user_tags_from_rpc_info(tag_details)
        fi_user_tag_list = list()
        for index in range(8):
            if index < len(user_tag_list):
                item = user_tag_list[index]
            else:
                item = None
            fi_user_tag_list.append(item)
        if log:
            print u"\t标签列表: %s" % fi_user_tag_list

        if log:
            print u'\tRPC time: %s, Result: %s' % (timedelta(seconds=(time.time() - rpc_time)), result)

    except Exception as e:
        print u"\t用户特征 %s ：异常 %s" % (uid, e)
        return None
    if log:
        print u"提取用户特征完成... time: %s" % timedelta(seconds=time.time() - s_time)
    return user_info_list + user_order_list + fi_user_tag_list


def get_doctor_features(did, log=False):
    """
    获取医生特征, [年龄, 性别, 职称, 图文价, 医院省份, 医院等级, 科室号]
    :param did: 医生ID
    :param log: 日志
    :return: 医生特征
    """
    if log:
        print "提取医生特征中... did: %s" % did
    s_time = time.time()
    try:
        params = {'doctor_ids': [did],
                  'fields': ['sex', 'born_date', 'hospital_province', 'hospital_grade',
                             'title', 'pro_price', 'clinic_no', 'second_class_clinic_no']}
        rpc_time = time.time()  # 统计RPC时间
        client = get_user_profile_service()
        result = client.getDoctorProfileInfo(json.dumps(params))
        did_info = json.loads(result)[did]
        [age, sex, level_title, pro_price, hospital_province, hospital_grade, clinic_no] = \
            get_doctor_info_from_rpc_info(did_info)
        if log:
            print u'\tRPC time: %s, Result: %s' % (timedelta(seconds=(time.time() - rpc_time)), result)
            print u'\t年龄: %s, 性别: %s, 职称: %s, 图文价: %s, 医院省份: %s, 医院等级: %s, 科室号: %s' % \
                  (age, sex, level_title, pro_price, hospital_province, hospital_grade, clinic_no)
    except Exception as e:
        print u"\t医生特征 %s ：异常 %s" % (did, e)
        return None
    if log:
        print "提取医生特征完成... time: %s" % timedelta(seconds=time.time() - s_time)
    return [age, sex, level_title, pro_price, hospital_province, hospital_grade, clinic_no]


def get_doctor_info_from_rpc_info(did_info):
    born_date = did_info.get('born_date', None)
    age = get_person_age(born_date) if born_date else -1  # 年龄数字
    sex = did_info.get('sex', 'u')  # 男m, 女f, 默认u
    level_title = did_info.get('title', None)
    pro_price = did_info.get('pro_price', -1)

    hospital_province = did_info.get('hospital_province', None)
    hospital_grade = did_info.get('hospital_grade', None)

    # 科室号, 优先子科室
    second_class_clinic_no = did_info.get('second_class_clinic_no', None)
    first_clinic_no = did_info.get('clinic_no', None)
    clinic_no = second_class_clinic_no if second_class_clinic_no else first_clinic_no

    return [age, sex, level_title, pro_price, hospital_province, hospital_grade, clinic_no]


def get_user_info_from_rpc_info(uid_info):
    born_date = uid_info.get('born_date', None)  # 生日日期
    age = get_person_age(born_date) if born_date else -1  # 年龄数字

    sex = uid_info.get('sex', None)  # 男m, 女f, 默认u
    province = uid_info.get('province', None)  # 省份汉字
    gold_coin = uid_info.get('gold_coin', -1)  # 金币数
    weight = uid_info.get('weight', -1.0)  # 体重
    height = uid_info.get('height', -1.0)  # 身高
    ehr_num = uid_info.get('ehr_num', -1)  # 档案数

    join_date = uid_info.get('join_date', None)  # 加入日期
    join_age = get_person_age(join_date) if join_date else -1  # 加入年数

    platform = uid_info.get('platform', -1)  # 1表示Android, 2表示iOS

    graph_total_num = uid_info.get('graph_total_num', -1)  # 图文总数
    graph_free_num = uid_info.get('graph_free_num', -1)  # 免费图文数
    graph_paid_num = uid_info.get('graph_paid_num', -1)  # 付费图文数
    graph_refund_num = uid_info.get('graph_refund_num', -1)  # 图文退款数
    graph_rebuy_num = uid_info.get('graph_rebuy_num', -1)  # 重复购买数
    graph_revisit_num = uid_info.get('graph_revisit_num', -1)  # 重复访问数
    assess_rating_num = uid_info.get('graph_assess_rating_num', -1)  # 图文评价数
    assess_rating_ratio = uid_info.get('graph_assess_rating_ratio', -1)  # 图文评价率
    assess_good_rating_num = uid_info.get('graph_assess_good_rating_num', -1)  # 图文好评数
    assess_good_rating_ratio = uid_info.get('graph_assess_good_rating_ratio', -1)  # 图片好评率
    reward_total_num = uid_info.get('reward_total_num', -1)  # 打赏总数
    reward_total_pay = uid_info.get('reward_total_pay', -1)  # 打赏总金额

    return [age, sex, province, gold_coin, weight, height, ehr_num, join_age, platform,
            graph_total_num, graph_free_num, graph_paid_num, graph_refund_num, graph_rebuy_num,
            graph_revisit_num, assess_rating_num, assess_rating_ratio, assess_good_rating_num, assess_good_rating_ratio,
            reward_total_num, reward_total_pay]


def get_user_order_from_rpc_info(paid_details):
    paid_sum = 0
    paid_num = 0
    paid_max = 0
    paid_min = 0
    paid_avg = 0.0
    g_paid_sum = 0
    g_paid_num = 0
    g_paid_max = 0
    g_paid_min = 0
    g_paid_avg = 0.0
    if paid_details:
        for paid_detail in paid_details:
            paid_type = paid_detail['type']
            if paid_type == 'total':
                paid_sum = paid_detail['pay']
                paid_num = paid_detail['num']
                paid_max = paid_detail['max']
                paid_min = paid_detail['min']
                paid_avg = paid_detail['avg']
            elif paid_type == 'graph':
                g_paid_sum = paid_detail['pay']
                g_paid_num = paid_detail['num']
                g_paid_max = paid_detail['max']
                g_paid_min = paid_detail['min']
                g_paid_avg = paid_detail['avg']
    return [paid_sum, paid_num, paid_max, paid_min, paid_avg,
            g_paid_sum, g_paid_num, g_paid_max, g_paid_min, g_paid_avg]


def get_user_tags_from_rpc_info(tag_details):
    tag_list = list()
    if not tag_details:
        return tag_list
    for tag_detail in tag_details:
        tag_list.append(tag_detail['name'])
    return tag_list


def get_search_info(query_text):
    json_param = json.dumps({'query': {'text': query_text, 'start': '0', 'rows': '1'}, 'filter': {}})
    data = get_search_service().search_doctors_for_debug(json_param)
    res_data = json.loads(data)
    return res_data


def get_word_intentions(query_text):
    """
    获取一个词的意图识别内容
    :param query_text: 查询词
    :return: 意图列表
    """
    res_data = get_search_info(query_text=query_text)
    intentions = res_data.get('intentionData').strip()
    res_list = intentions.split(' ')
    return res_list


def test_of_get_user_features():
    """
    测试提取用户特征的接口
    :return: None
    """
    print "-" * 50
    uid = "44904932"  # 优质用户
    # uid = "95388224"  # 数据较全用户
    print get_user_features(uid=uid, log=True)
    print "-" * 50


def test_of_get_doctor_features():
    """
    测试提取医生特征的接口
    :return: None
    """
    print "-" * 50
    # did = "clinic_web_8ef2c150704aa70f"
    did = "clinic_web_dea197d753d3c2ae"
    print get_doctor_features(did=did, log=True)
    print "-" * 50


def test_of_get_word_intentions():
    """
    测试搜索的意图识别
    :return: None
    """
    res = get_word_intentions(query_text=u'感冒')
    print list_2_utf8(res)


def test_of_get_users_province():
    uid_list = ['2413643', '57179481']
    res = get_users_province(uid_list)
    print res


if __name__ == "__main__":
    # test_of_get_user_features()  # 测试用户
    # test_of_get_doctor_features()  # 测试医生
    # test_of_get_word_intentions()  # 测试意图识别
    test_of_get_users_province()  # 测试用户省份
