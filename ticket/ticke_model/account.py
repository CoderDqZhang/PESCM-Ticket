#coding=utf-8
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from ticket.ticke_model.department import Department

class AccountGroup(models.Model):
    group_id = models.IntegerField('群组ID',auto_created=True,primary_key=True)
    group_status = models.IntegerField('群组分布ID',default=0) #群组状态 0关闭，1开启
    group_name = models.CharField('群组名称',max_length=255,null=False,blank=False)
    group_menu = models.CharField('人员级别',max_length=255,null=False,blank=False)

    def __str__(self):
        return self.group_name + '-' + self.group_menu

class Account(models.Model):
    nickname = models.CharField('用户名', max_length=255, default='', null=True) #用户名
    user_id = models.CharField('用户id', primary_key=True, max_length=10,
                               default='', null=False, blank=False) #用户ID
    email = models.EmailField('邮件地址',max_length=254, null=True,blank=True)
    password = models.CharField('密码', max_length=16, default='123456', null=False) #密码
    department = models.ForeignKey(Department,verbose_name='部门',on_delete=models.CASCADE)#多对一（博客--类别）
    group = models.ForeignKey(AccountGroup, verbose_name='群组', on_delete=models.CASCADE,null=True)  # 多对一（博客--类别）
    status = models.IntegerField('甲乙区分', default = 0, null=True) #甲乙区分 0代表甲方，1代表乙方
    desc = models.CharField('负责项目', max_length=255, default='', null=True) #人员介绍
    create_time = models.DateTimeField('创建时间',auto_created=True,auto_now=True) #创建时间
    last_login = models.DateTimeField('最后登录时间',auto_created=False,auto_now=False) #最后登录时间
    avatar = models.ImageField('头像', upload_to="avatar/%Y/%m", default=u"image/default.png", blank=True, null=True)

    def __str__(self):
        return self.nickname

    #显示群组&用户级别
    def show_user_lv(self):
        return self.group.group_name + '-' + self.group.group_menu



