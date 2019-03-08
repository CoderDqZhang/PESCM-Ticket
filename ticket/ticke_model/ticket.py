# coding=utf-8
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from ticket.ticke_model.department import Department
from ticket.ticke_model.account import Account
from ticket.ticke_model.category import TicketModel
import django.utils.timezone as timezone
import datetime


class TicketConfim(models.Model):
    user = models.ForeignKey(Account, verbose_name='处理人员', on_delete=models.CASCADE)
    status = models.IntegerField('处理状态', default=0)  # 状态 0未处理，1处理完成
    # 是否是转派过来的工单
    transfer = models.IntegerField('是否转派', default=0)  # 状态 0否，1是（处理完成后转派给他人），2，接到转派工单

    content = models.TextField('处理描述', null=True, blank=True)
    confirm_time = models.DateTimeField('处理时间', auto_created=False, null=True, blank=True, auto_now=False)

    confirm_remark = models.TextField('处理人工单备注', help_text='处理人工单备注', max_length=255, null=True, blank=False,
                                      default='')  # 问题及现状描述

    confirm_file = models.FileField(upload_to="handle/%Y/%m/%d", null=True, )
    file_name = models.CharField('文件名称', max_length=255, null=True, default='None')

    handel_time = models.FloatField('执行天数', default=0.0)  # 创建工单者执行天数
    check = models.IntegerField('是否审核',default=0) # 状态 0否，1是

    def __str__(self):
        return self.user.nickname


class Ticket(models.Model):
    ticket_show_id = models.CharField('工单显示ID', default='', null=False, blank=False, max_length=255)

    ticket_id = models.AutoField('工单ID', primary_key=True, null=False, blank=False)
    ticket_title = models.CharField('工单标题', help_text='输入工单标题', max_length=255, null=False, blank=False)
    ticket_desc = models.TextField('工单描述', help_text='输入工单详细描述', max_length=255, null=True, blank=False,
                                   default='')  # 问题及现状描述
    ticket_model_ticket = models.ForeignKey(TicketModel, verbose_name='工单模型', on_delete=models.CASCADE)  # 问题类别
    ticket_lev = models.IntegerField('紧急状态', default=0)  # 状态，一般，紧急，
    ticket_status = models.IntegerField('工单状态', default=0)  # 状态0 未处理，1处理中，2工单驳回，3处理完成。
    ticket_listsort = models.ManyToManyField(TicketConfim, '工单处理人员', null=False, blank=False)  # 实施顾问
    ticket_create_user = models.ForeignKey(Account, '创建人', null=False, blank=False)  # 提报人
    create_time = models.DateTimeField('创建时间', auto_created=True, auto_now=True)  # 提报时间

    ticket_file = models.FileField(upload_to="ticket/%Y/%m/%d", null=True)  # 提交附件
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

    # 显示工单的状态
    def show_status(self):
        if self.ticket_status == 3:
            return '完成'
        else:
            return '未完成'

    #显示工单的紧急状态与否
    def show_ticket_lev(self):
        if self.ticket_lev == 0:
            return '一般'
        else:
            return '紧急'

    #工单创建时间到测试机部署时间的时间间隔
    def create_todev_time(self):
        time1 = datetime.datetime.strptime(self.dev_push_time.strftime('%Y-%m-%d'), "%Y-%m-%d")
        time2 = datetime.datetime.strptime(self.create_time.strftime('%Y-%m-%d'), "%Y-%m-%d")
        return (time1.date() - time2.date()).total_seconds()/(24*60*60)
