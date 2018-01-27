#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试MySQL数据库

Created by C.L.Wang
"""
import os

from django.db import ConnectionHandler

from configs import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "configs.settings")


def test_mysql():
    connections = ConnectionHandler(settings.DATABASES)
    cursor = connections['core_db'].cursor()
    # sql = "select * from symptomchecker_doctor limit 1"
    sql = "select initial_query,rewrite_query,type_choice from medicaldb_searchqueryrewrite limit 1"
    cursor.execute(sql)
    row = cursor.fetchone()
    print row


if __name__ == '__main__':
    test_mysql()
