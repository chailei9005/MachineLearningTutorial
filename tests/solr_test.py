#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试Solr接口

Created by C.L.Wang
"""
import pysolr

from configs.solr_configs import TEST_SOLR_DOCTORS


def cy_solr_in_main_doctors(doctors):
    """
    批量的Solr搜索
    :param doctors: 医生列表
    :return: 医生信息字典
    """
    ids_str = ""
    for did in doctors:
        ids_str += ("%s " % unicode(did))
    query = 'id:(%s)' % ids_str
    solr = pysolr.Solr(TEST_SOLR_DOCTORS)  # 测试
    # solr = pysolr.Solr(ONLINE_SOLR_DOCTORS)  # 线上
    search_params = {"fl": "id,cust_star_p", "rows": 10}  # 只输出几个内容
    result = solr.search(query, **search_params)
    res_dict = dict()
    for doc in result.docs:
        score = doc.get('cust_star_p', None)
        id = doc.get('id', None)
        res_dict[id] = score
    return res_dict


def test_of_cy_solr_in_main_doctors():
    doctors = [u'clinic_web_9b639114f380ba19', 'clinic_web_cbe362ce513b94b1', 'clinic_web_45e0f9b9c5a50d25']
    print cy_solr_in_main_doctors(doctors)


if __name__ == '__main__':
    test_of_cy_solr_in_main_doctors()
