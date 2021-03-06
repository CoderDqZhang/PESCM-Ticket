# coding=utf-8
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from ticket.ticke_model.department import Department
from ticket.ticke_model.account import Account,AccountGroup
from ticket.ticke_model.category import TicketModel
import django.utils.timezone as timezone
import datetime


CONFIRM_STATUS = (
    ('0','未处理'),
    ('1','完成'),
)

TRANSFER = (
    ('0','未转派'),
    ('1','已转派'),
    ('2','被转派')
)

CHECK = (
    ('0','未审核'),
    ('1','已审核')
)

class TicketConfim(models.Model):
    user = models.ForeignKey(Account, verbose_name='处理人员', on_delete=models.CASCADE)
    status = models.CharField('处理状态', max_length=7, default='0', choices=CONFIRM_STATUS)  # 状态 0未处理，1处理完成
    # 是否是转派过来的工单
    transfer = models.CharField('是否转派', max_length=7, default='0', choices=TRANSFER)  # 状态 0否，1是（处理完成后转派给他人），2，接到转派工单

    content = models.TextField('处理描述', null=True, blank=True)
    confirm_time = models.DateTimeField('处理时间', auto_created=False, null=True, blank=True, auto_now=False)

    confirm_remark = models.TextField('处理人工单备注', help_text='处理人工单备注', max_length=255, null=True, blank=False,
                                      default='')  # 问题及现状描述

    confirm_file = models.FileField(upload_to="handle/%Y/%m/%d", null=True, )
    file_name = models.CharField('文件名称', max_length=255, null=True, default='None')

    handel_time = models.FloatField('执行天数', default=0.0)  # 创建工单者执行天数
    check = models.CharField('是否审核',max_length=7, default='0', choices=CHECK) # 状态 0否，1是

    def __str__(self):
        return self.user.nickname


TICKET_LV = (
    ('0','一般'),
    ('1','紧急'),
)

TICKET_STATUS = (
    ('0','未处理'),
    ('1','处理中'),
    ('2','工单驳回'),
    ('3','处理完成')
)

class Ticket(models.Model):
    ticket_show_id = models.CharField('工单显示ID', default='', null=False, blank=False, max_length=255)

    ticket_id = models.AutoField('工单ID', primary_key=True, null=False, blank=False)
    ticket_title = models.CharField('工单标题', help_text='输入工单标题', max_length=255, null=False, blank=False)
    ticket_desc = models.TextField('工单描述', help_text='输入工单详细描述', max_length=255, null=True, blank=False,
                                   default='')  # 问题及现状描述
    ticket_model_ticket = models.ForeignKey(TicketModel, verbose_name='工单模型', on_delete=models.CASCADE)  # 问题类别
    ticket_lev = models.CharField('紧急状态', max_length=255, default = '0', choices=TICKET_LV)  # 状态，一般，紧急，
    ticket_status = models.CharField('工单状态', max_length=255, default='0', choices=TICKET_STATUS)  # 状态0 未处理，1处理中，2工单驳回，3处理完成。
    ticket_listsort = models.ManyToManyField(TicketConfim, verbose_name='工单处理人员', null=False, blank=False)  # 实施顾问
    ticket_create_user = models.ForeignKey(Account, verbose_name='创建人',on_delete=models.CASCADE, null=False, blank=False)  # 提报人
    create_time = models.DateTimeField('创建时间', auto_created=True, auto_now=True)  # 提报时间

    ticket_file = models.FileField(upload_to="ticket/%Y/%m/%d",verbose_name='文件', null=True)  # 提交附件
    file_name = models.CharField('文件名称', max_length=255, null=True, default='None')

    ticket_remark = models.TextField('工单备注', help_text='工单备注', max_length=255, null=True, blank=False,
                                     default='')  # 问题及现状描述
    handel_time = models.FloatField('预期天数', default=0.0)  # 创建工单者执行天数
    done_time = models.FloatField('实际执行天数', default=0.0)  # 实际执行天数

    dev_push_time = models.DateField('测试机部署时间', auto_created=False, auto_now_add=False, null=True,
                                     blank=True)  # 测试机部署时间
    pub_push_time = models.DateField('生产机部署时间', auto_created=False, auto_now_add=False, null=True,
                                     blank=True)  # 生产机部署时间


    def __str__(self):
        return self.ticket_title

    #工单创建时间到测试机部署时间的时间间隔
    def create_todev_time(self):
        time1 = datetime.datetime.strptime(self.dev_push_time.strftime('%Y-%m-%d'), "%Y-%m-%d")
        time2 = datetime.datetime.strptime(self.create_time.strftime('%Y-%m-%d'), "%Y-%m-%d")
        return (time1.date() - time2.date()).total_seconds()/(24*60*60)
