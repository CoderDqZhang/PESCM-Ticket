#coding=utf-8
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from ticket.ticke_model.department import Department
from ticket.ticke_model.account import Account
from ticket.ticke_model.category import TicketModel

class TicketConfim(models.Model):
    user = models.ForeignKey(Account,verbose_name='处理人员',on_delete=models.CASCADE)
    status = models.IntegerField('处理状态',default=0) #状态 0未处理，1处理完成
    #是否是转派过来的工单
    transfer = models.IntegerField('是否转派',default=0) #状态 0否，1是（处理完成后转派给他人），2，接到转派工单

    content = models.TextField('处理描述',null=True,blank=True)
    confirm_time = models.DateTimeField('处理时间',auto_created=False,null=True,blank=True,auto_now=False)

    confirm_file = models.FileField(upload_to="handle/%Y/%m/%d",null=True,)
    file_name = models.CharField('文件名称',max_length=255,null=True,default='None')

    def __str__(self):
        return self.user.nickname

class Ticket(models.Model):
    ticket_id = models.AutoField('工单ID', primary_key=True, null=False,blank=False)
    ticket_title = models.CharField('工单标题',help_text='输入工单标题',max_length=255, null=False,blank=False)
    ticket_desc = models.TextField('工单描述',help_text='输入工单详细描述',max_length=255, null=True,blank=False,default='')
    ticket_model_ticket = models.ForeignKey(TicketModel,verbose_name='工单模型',on_delete=models.CASCADE)
    ticket_lev = models.IntegerField('紧急状态',default=0) #状态，一般，紧急，
    ticket_status = models.IntegerField('工单状态',default=0) #状态0 未处理，1处理中，2工单驳回，3处理完成。
    ticket_listsort = models.ManyToManyField(TicketConfim,'工单处理人员',null=False,blank=False)
    ticket_create_user = models.ForeignKey(Account,'创建人',null=False,blank=False)
    create_time = models.DateTimeField('创建时间',auto_created=True,auto_now=True)

    ticket_file = models.FileField(upload_to="ticket/%Y/%m/%d", null=True)
    file_name = models.CharField('文件名称', max_length=255, null=True, default='None')

    def __str__(self):
        return self.ticket_title
