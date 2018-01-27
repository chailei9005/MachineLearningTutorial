#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
邮件发送

Created by C.L.Wang
"""
import os

import sys

reload(sys)
sys.setdefaultencoding('utf-8')  # 避免编码错误

from django.core.mail import EmailMultiAlternatives

from configs.configs import EmailConfigs
from project_utils import get_current_time_str
from rcm_doctors.constants import RESULT_DIR
from root_dir import ROOT_DIR

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "configs.settings")

"""
注意: Django版本的较低, 如1.3.4, 影响中文邮件的发送
升级最新的Django-1.11.9, 问题解决
"""


def send_html_mail(subject, message, sender, recipient, html_message=None, attachment=None):
    """
    send HTML message
    """
    mail = EmailMultiAlternatives(subject, message, sender, recipient)
    if html_message:
        mail.attach_alternative(html_message, 'text/html')
    if attachment:
        mail.attach_file(attachment, 'text/html')
    mail.send()


def send_html_mail_with_attaches(subject, message, sender, recipient, html_message=None, attach_list=None):
    """
    send HTML message
    """
    mail = EmailMultiAlternatives(subject, message, sender, recipient)
    if html_message:
        mail.attach_alternative(html_message, 'text/html')
    if attach_list:
        for attachment in attach_list:
            mail.attach_file(attachment, 'text/html')
    mail.send()


if __name__ == '__main__':
    wf_name = os.path.join(ROOT_DIR, RESULT_DIR, '省份统计数据.zip')
    send_html_mail(subject=u'医生未回复问题定时任务',
                   message=u'发送时间: %s, 行数: %s' % (get_current_time_str(), 100),
                   sender=EmailConfigs.SYS_EMAIL,
                   recipient=[EmailConfigs.MY_EMAIL],
                   attachment=wf_name)
