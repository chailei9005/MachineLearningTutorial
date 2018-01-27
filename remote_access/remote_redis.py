#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Redis缓存数据

Created by C.L.Wang
"""
import os
import sys

p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if p not in sys.path:
    sys.path.append(p)

from cy_cache.django_model.custom_redis import CustomRedis

from configs.configs import RedisConf

persist_redis = CustomRedis(
    host=RedisConf.persist_host,
    port=RedisConf.persist_port,
    password=RedisConf.persist_password)


class DoctorUnanswerBatchGetCache(object):
    """
    医生未回复问题个数,批量获取用
    NOTICE:这个东西没有引用也不要删除,也许在 medweb 里没有用, 在其他项目里用
    """
    EXPIRE_TIME = 30 * 24 * 60 * 60  # 有效期30天

    @classmethod
    def build_unanswered_key(cls, to_doc):
        return 'doctor_unanswered_key_20160526_%s' % to_doc

    @classmethod
    def hmget_lt_max_num_doctor_ids(cls, doctor_id_list, to_doc=True, num_limit=1):
        if not isinstance(doctor_id_list, list):
            doctor_id_list = list(doctor_id_list)
        key = cls.build_unanswered_key(to_doc)

        nums = persist_redis.hmget(key, doctor_id_list) if doctor_id_list else []

        return [doctor_id for doctor_id, num in zip(doctor_id_list, nums) if not num or int(num) <= num_limit]

    @classmethod
    def get_count(cls, doctor_id, to_doc=True):
        """
        获取医生未回复数量
        """
        key = cls.build_unanswered_key(to_doc)
        return int(persist_redis.hget(key, doctor_id) or 0)


def get_dct_unanswer(dct_id):
    """
    在Redis中获取医生的未回复问题数, 本地测试无效, 服务器有效
    需要导入线上的Settings.py
    :param dct_id: 医生ID
    :return: 医生未回复问题数
    """
    dct_redis = DoctorUnanswerBatchGetCache()
    return dct_redis.get_count(dct_id)


def test_get_dct_unanswer():
    dct_id = 'clinic_web_02090551007511e0'  # 李洁
    print get_dct_unanswer(dct_id)


if __name__ == '__main__':
    test_get_dct_unanswer()
