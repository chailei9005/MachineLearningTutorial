#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
远程的Solr服务

Created by C.L.Wang
"""
import pysolr

from configs.configs import SolrConf
from project_utils import *


def get_search_words(num, time_str='2017-12-17'):
    """
    获取Top N的搜索词
    2017.11.18 ~ 2017.12.18
    最新时间: 2018/1/18 23:59:57
    :param num: 获取词数
    :param time_str: 时间字符串
    :return: 词列表
    """
    timestamp = timestr_2_timestamp(time_str=time_str)
    print "\t\t时间: %s, 时间戳: %s" % (time_str, timestamp)
    solr = pysolr.Solr(SolrConf.TEST_SOLR_SEARCH)  # 测试
    query = '*:*'
    search_params = {'rows': 1, 'fq': 'event_time: [%s TO *]' % timestamp,
                     'facet.field': 'text', 'facet': 'on', 'facet.limit': num}  # 只输出几个内容
    result = solr.search(query, **search_params)
    facets = result.facets.get('facet_fields').get('text')
    word_dict = dict()
    for word, count in grouped_list(facets, 2):
        word_dict[word] = count
    return word_dict


if __name__ == '__main__':
    print list_2_utf8(get_search_words(10))  # 测试前10个搜索词
