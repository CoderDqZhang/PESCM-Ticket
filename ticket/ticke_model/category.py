#coding=utf-8
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from ticket.ticke_model.department import Department
from ticket.ticke_model.account import Account

class Category(models.Model):
    category_id = models.IntegerField('问题类型ID',auto_created=True,primary_key=True,null=False,blank=False)
    category_name = models.CharField('问题描述',max_length=255,null=False,blank=False)
    category_desc = models.TextField('详细描述',max_length=255,null=True,blank=True)
    category_create_time = models.DateField('创建时间',auto_created=True,auto_now=True)

    def __str__(self):
        return self.category_name

class TicketModel(models.Model):
    ticket_id = models.IntegerField('问题类型ID',primary_key=True,null=False,blank=False)
    ticket_model = models.ForeignKey(Category,verbose_name='问题分类',on_delete=models.CASCADE)
    ticket_model_name = models.CharField('问题描述', max_length=255, null=False, blank=False)
    ticket_model_desc = models.TextField('详细描述', max_length=255, null=True, blank=True)
    ticket_model_create_time = models.DateField('创建时间', auto_created=True, auto_now=True)

    def __str__(self):
        return self.ticket_model_name