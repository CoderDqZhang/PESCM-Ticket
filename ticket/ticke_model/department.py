#coding=utf-8
from __future__ import unicode_literals
from django.db import models

class Department(models.Model):
    partment_code = models.CharField('部门ID',max_length=10, default='000000',
                                   primary_key=True,null=False,blank=False)
    partment_desc = models.CharField('部门名称',max_length=255,default='',null=False,blank=False)
    partment_lev =  models.IntegerField('部门级别',default=0)


    def __str__(self):
        return self.partment_desc