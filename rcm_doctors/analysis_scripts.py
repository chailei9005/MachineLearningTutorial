#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
分析脚本的集合

Created by C.L.Wang
"""

import os
import sys

import pysolr
import xlsxwriter
from django.db import ConnectionHandler

from configs import settings
from remote_access.remote_apis import get_word_intentions
from remote_access.remote_solr import get_search_words

p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if p not in sys.path:
    sys.path.append(p)

from remote_access.remote_email import send_html_mail

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "configs.settings")

from remote_access.remote_redis import get_dct_unanswer
from configs.configs import SolrConf, EmailConfigs
from project_utils import *
from rcm_doctors.constants import DATA_DIR, RESULT_DIR
from root_dir import ROOT_DIR

"""
用户省份类别: 31, 医生省份类别: 32
["上海市", "云南省", "内蒙古自治区", "北京市", "吉林省", "四川省", "天津市", "宁夏回族自治区", "安徽省", "山东省", "山西省", 
"广东省", "广西壮族自治区", "新疆维吾尔自治区", "江苏省", "江西省", "河北省", "河南省", "浙江省", "海南省", "湖北省", "湖南省", 
"甘肃省", "福建省", "西藏自治区", "贵州省", "辽宁省", "重庆市", "陕西省", "青海省", "黑龙江省"]
["上海市", "云南省", "内蒙古自治区", "北京市", "吉林省", "四川省", "天津市", "宁夏回族自治区", "安徽省", "山东省", "山西省",
 "广东省", "广西壮族自治区", "新疆维吾尔自治区", "江苏省", "江西省", "河北省", "河南省", "浙江省", "海南省", "湖北省", "湖南省", 
 "澳门特别行政区", "甘肃省", "福建省", "西藏自治区", "贵州省", "辽宁省", "重庆市", "陕西省", "青海省", "黑龙江省"]
"""

PROVINCE_SIMPLIFY = {
    u'四川': u'四川省',
    u'山东': u'山东省',
    u'河南': u'河南省',
    u'福建': u'福建省',
    u'浙江': u'浙江省',
    u'山西': u'山西省',
    u'辽宁': u'辽宁省',
    u'陕西': u'陕西省',
    u'黑龙江': u'黑龙江省',
    u'深圳': u'广东省',
    u'广西省': u'广西壮族自治区',
    u'新疆': u'新疆维吾尔自治区',
    u'澳门': u'澳门特别行政区',
    u'江苏省苏州市': u'江苏省',
    u'Bangkok': u'None'
}


def analysis_same_province(rf_name, wf_name):
    """
    统计购买数据中用户和医生的相同省份
    :param rf_name 读取文件
    :param wf_name 写入文件
    :return: 省份数据
    """
    print "\t数据文件: %s" % rf_name
    lines = read_file(rf_name)
    print "\t文件行数: %s" % len(lines)
    if not lines:
        print "\t文件为空!"
    tmp_line = lines[0].split(',')
    print "\t数据维度: %s" % len(tmp_line)
    print "\t用户省份: %s, 医生省份: %s" % (tmp_line[4], tmp_line[45])

    user_dict = collections.defaultdict(int)  # 统计用户省份数据
    doctor_dict = collections.defaultdict(int)  # 统计医生省份数据
    same_dict = collections.defaultdict(int)  # 相同的省份数

    count = 0  # 总数
    same_count = 0  # 相同数
    for line in lines:
        line_data = line.split(",")
        user_province = unicode(line_data[4]).strip()
        doctor_province = unicode(line_data[45]).strip()

        if doctor_province in PROVINCE_SIMPLIFY:  # 处理省份简写
            doctor_province = PROVINCE_SIMPLIFY[doctor_province]
        if user_province in PROVINCE_SIMPLIFY:  # 处理省份简写
            user_province = PROVINCE_SIMPLIFY[user_province]

        if user_province == 'None' or doctor_province == 'None' or doctor_province == 'Bangkok':
            continue

        user_dict[user_province] += 1
        doctor_dict[doctor_province] += 1

        if user_province == doctor_province:
            same_count += 1
            same_dict[user_province] += 1

        count += 1
        if count % 10000 == 0:
            print "\t\tcount %s" % count

    print "用户省份类别: %s, 医生省份类别: %s" % (len(user_dict.keys()), len(doctor_dict.keys()))
    print list_2_utf8(sorted(user_dict.keys()))
    print list_2_utf8(sorted(doctor_dict.keys()))

    print "总数: %s, 相同数: %s, 占比: %0.2f%%" % (count, same_count, calculate_percent(same_count, count))

    result_list = [count, same_count, '%0.2f%%' % calculate_percent(same_count, count)]  # 结果行
    write_result_for_sp(wf_name, user_dict, doctor_dict, same_dict, result_list)  # 写入文件


def write_result_for_sp(wf_name, user_dict, doctor_dict, same_dict, result_list):
    """
    写入Excel文件, 方便阅读
    :param wf_name: 写入文件名
    :param user_dict: 用户省份字典
    :param doctor_dict: 医生省份字典
    :param same_dict: 相同字典
    :param result_list: 结果列
    :return: 写入文件
    """
    workbook = xlsxwriter.Workbook(wf_name)
    worksheet = workbook.add_worksheet()
    title_line = [u'']
    title_list = max_list(user_dict.keys(), doctor_dict.keys())
    for t_item in title_list:
        title_line.append(t_item)
    worksheet.write_row(0, 0, title_line)  # 写入标题

    # 统计数字
    user_data_list = list()
    doctor_data_list = list()
    same_data_list = list()
    for title in title_line:
        if title == u'':
            user_data_list.append(u'用户')
            doctor_data_list.append(u'医生')
            same_data_list.append(u'相同')
            continue
        user_data_list.append(user_dict.get(title, 0))
        doctor_data_list.append(doctor_dict.get(title, 0))
        same_data_list.append(same_dict.get(title, 0))

    worksheet.write_row(1, 0, user_data_list)
    worksheet.write_row(2, 0, doctor_data_list)
    worksheet.write_row(3, 0, same_data_list)
    worksheet.write_row(4, 0, [])
    worksheet.write_row(5, 0, [u'总数', u'相同数', u'占比'])
    worksheet.write_row(6, 0, result_list)

    workbook.close()


def max_list(list1, list2):
    if len(list1) > len(list2):
        return list1
    else:
        return list2


def save_all_doctors(out_file):
    """
    存储全部大于3000分的医生
    :param out_file 输出文件
    :return: 医生文件
    """
    print "\t写入文件: %s" % out_file
    if os.path.exists(out_file):
        print "文件存在，删除文件：%s" % out_file
        os.remove(out_file)  # 删除已有文件

    solr = pysolr.Solr(SolrConf.TEST_SOLR_DOCTORS)  # 测试
    query = '*:*'
    search_params = {'fq': 'cust_star:[2500 TO *]', 'fl': 'id,name,cust_star', 'sort': 'cust_star desc',
                     'rows': 10000}  # 只输出几个内容
    result = solr.search(query, **search_params)

    count = 0
    for doc in result.docs:
        # print list_2_utf8(doc)
        did = str(doc.get('id', None))
        name = str(doc.get('name', None))
        cust_star = str(doc.get('cust_star', None))
        line_str = ','.join([did, name, cust_star])
        write_line(out_file, line_str)
        count += 1
        if count % 1000 == 0:
            print "count %s" % count

    print "\t写入全部医生! count %s" % count


def output_doctors_unanswer(df_name, wf_name):
    """
    输出医生的未回复问题数
    :param df_name: 医生文件 
    :param wf_name: 写入文件 
    :return: 写入文件
    """
    print "\t读取医生文件: %s" % df_name
    print "\t写入医生文件: %s" % wf_name
    data_lines = read_file(df_name)
    print "\t统计医生总数: %s" % len(data_lines)

    did_name_dict = dict()
    did_unanswer_dict = dict()
    for data_line in data_lines:
        [did, name, score] = data_line.split(',')
        did_name_dict[did] = name
        unanswer_num = get_dct_unanswer(did)
        if unanswer_num > 0:  # 只统计大于0的医生
            did_unanswer_dict[did] = unanswer_num

    write_result_for_doctors_unanswer(wf_name, did_name_dict, did_unanswer_dict)  # 写入文件


def write_result_for_doctors_unanswer(wf_name, did_name_dict, did_unanswer_dict):
    """
    将医生的未回复问题数据, 写入Excel文件
    
    :param wf_name: 输出文件名
    :param did_name_dict: 医生姓名字典
    :param did_unanswer_dict: 医生未回复问题字典
    :return: 写入文件
    """
    workbook = xlsxwriter.Workbook(wf_name)
    worksheet = workbook.add_worksheet()
    worksheet.write_row(0, 0, [u'姓名', u'ID', u'未答数'])  # 写入标题

    count = 1
    did_unanswer_list = sort_dict_by_value(did_unanswer_dict)
    for (did, unanswer_num) in did_unanswer_list:
        data_line = [did_name_dict.get(did), did, unanswer_num]
        worksheet.write_row(count, 0, data_line)
        count += 1
    workbook.close()  # 关闭文件
    print "\t写入文件完成! 行数: %s" % count

    # 发送邮件
    send_html_mail(u'医生未回复问题定时任务',
                   u'发送时间: %s, 行数: %s' % (get_current_time_str(), count),
                   EmailConfigs.SYS_EMAIL,
                   # [EmailConfigs.MY_EMAIL],  # 自己的测试邮件
                   EmailConfigs.MY_PARTNERS_EMAILS,  # 其他人的邮件组合
                   attachment=wf_name)


def save_words_intentions(file_name):
    """
    存储词的意图
    :return: 搜索词频
    """
    print "\t写入文件: %s" % file_name
    if os.path.exists(file_name):
        print "文件存在，删除文件：%s" % file_name
        os.remove(file_name)  # 删除已有文件
    word_num = 5000
    word_dict = get_search_words(word_num)
    word_list = sort_dict_by_value(word_dict)
    res_list = list()
    for (word, word_times) in word_list:
        res_list.append([word, word_times, list_2_utf8(get_word_intentions(word))])
    write_res_for_wi(file_name, res_list)


def write_res_for_wi(wf_name, res_list):
    workbook = xlsxwriter.Workbook(wf_name)
    worksheet = workbook.add_worksheet()
    worksheet.write_row(0, 0, [u'搜索词', u'频次', u'意图'])
    count = 1
    for res_data in res_list:
        worksheet.write_row(count, 0, res_data)
        count += 1
        if count % 200 == 0:
            print "count %s" % count
    workbook.close()
    print "\t写入文件完成! 行数: %s" % count


def save_synonym_file(wf_name):
    """
    保存同义词文件
    :return: 同义词
    """
    connections = ConnectionHandler(settings.DATABASES)
    cursor = connections['dependency_db'].cursor()
    sql = "select initial_query,rewrite_query,type_choice from medicaldb_searchqueryrewrite"
    cursor.execute(sql)
    rows = cursor.fetchall()
    workbook = xlsxwriter.Workbook(wf_name)
    worksheet = workbook.add_worksheet()
    worksheet.write_row(0, 0, [u'同义词列表'])
    count = 1
    for row in rows:
        line_type = row[2]
        if line_type != 0:
            worksheet.write_row(count, 0, row[0:-1])
            count += 1
            if count % 200 == 0:
                print "count %s" % count
    workbook.close()
    print "\t写入文件完成! 行数: %s" % count


def load_doctors_from_sj_by_solr():
    """
    加载三甲医院的医生
    :return: 医生列表
    """
    solr = pysolr.Solr(SolrConf.TEST_SOLR_DOCTORS)
    query = 'hospital_grade:"三级甲等"'
    search_params = {'fl': 'id,name,cust_star_p', 'sort': 'score desc,cust_star_p desc', 'rows': 20}
    res = solr.search(q=query, **search_params)
    res_docs = res.docs
    print list_2_utf8(res_docs)


def load_doctors_from_good_hsp_by_solr():
    """
    加载知名医院医生, 需要重新建立hospital_weight的索引
    :return: 医生列表
    """
    solr = pysolr.Solr(SolrConf.TEST_SOLR_DOCTORS)
    query = 'hospital_weight:"1.15"'
    search_params = {'fl': 'id,name,hospital_name,cust_star_p', 'sort': 'score desc,cust_star_p desc', 'rows': 20}
    res = solr.search(q=query, **search_params)
    res_docs = res.docs
    print list_2_utf8(res_docs)


def test_of_analysis_same_province():
    """
    分析在购买、点击、展示中，用户和医生省份数据相同的个数
    
    :return: 写入文件
    """
    # 购买
    # rf_name = os.path.join(ROOT_DIR, DATA_DIR, "train_purchase_20170101_20171120")
    # wf_name = os.path.join(ROOT_DIR, RESULT_DIR, "purchase_analysis_same_province_%s.xlsx" % get_current_time_str())
    # analysis_same_province(rf_name, wf_name)

    # 点击
    # rf_name2 = os.path.join(ROOT_DIR, DATA_DIR, "train_click_20170101_20171120")
    # wf_name2 = os.path.join(ROOT_DIR, RESULT_DIR, "click_analysis_same_province_%s.xlsx" % get_current_time_str())
    # analysis_same_province(rf_name2, wf_name2)

    # 展示
    rf_name3 = os.path.join(ROOT_DIR, DATA_DIR, "train_show_20170101_20171120")
    wf_name3 = os.path.join(ROOT_DIR, RESULT_DIR, "show_analysis_same_province_%s.xlsx" % get_current_time_str())
    analysis_same_province(rf_name3, wf_name3)


def test_of_save_all_doctors():
    """
    存储全部医生数据, 保证医生数据一致性
    :return: 写入文件
    """
    all_doctors = os.path.join(ROOT_DIR, DATA_DIR, 'all_doctors.txt')
    save_all_doctors(all_doctors)


def test_of_output_doctors_unanswer():
    """
    测试未回复问题脚本
    :return: 写入文件
    """
    print '-' * 50
    print "执行时间: %s" % get_current_time_for_show()
    all_doctors = os.path.join(ROOT_DIR, DATA_DIR, 'all_doctors.txt')
    out_folder = os.path.join(ROOT_DIR, RESULT_DIR, 'data_of_unanswers')
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)
        print '文件夹 "%s" 不存在，创建文件夹。' % out_folder
    out_file = os.path.join(out_folder, 'doctor_unanwser_%s.xlsx' % get_current_time_str())
    output_doctors_unanswer(all_doctors, out_file)
    print '-' * 50


def test_of_save_words_intentions():
    wf_file = os.path.join(ROOT_DIR, RESULT_DIR, "search_words_with_intentions.xlsx")
    save_words_intentions(wf_file)


def test_of_save_synonym_file():
    wf_file = os.path.join(ROOT_DIR, RESULT_DIR, "synonyms.xlsx")
    save_synonym_file(wf_file)


if __name__ == '__main__':
    # test_of_analysis_same_province()  # 统计购买数据中用户和医生的相同省份
    # test_of_save_all_doctors()  # 存储全部医生
    # test_of_output_doctors_unanswer()  # 输出全部未回复医生数
    # test_of_save_words_intentions()  # 存储疾病词的意图识别
    # test_of_save_synonym_file()  # 存储同义词文件
    load_doctors_from_sj_by_solr()  # 加载三甲医院的医生
    load_doctors_from_good_hsp_by_solr()  # 加载知名医院医生
