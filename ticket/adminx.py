# -*- coding: utf-8 -*-
# encoding=utf8
import sys
import importlib
importlib.reload(sys)

import xadmin
import xadmin.views as xviews
from xadmin.plugins.auth import UserAdmin
from xadmin.layout import Fieldset, Main, Side, Row
from django.utils.translation import ugettext as _
from ticket.ticke_model.account import Account,AccountGroup
from ticket.ticke_model.department import Department
from ticket.ticke_model.category import TicketModel,Category
from ticket.ticke_model.ticket import Ticket
from django.forms import widgets
from PESCM import settings
from xadmin.views.base import ModelAdminView, filter_hook, csrf_protect_m
from mdeditor.widgets import MDEditorWidget

class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True

class GlobalSettings(object):
    enable_themes = True
    site_title = "PESCM后台管理"
    site_footer = "PESCM后台管理"
    # menu_style = 'accordion'

    # 菜单设置

    def get_site_menu(self):
        return (

            {'title': '数据类型', 'perm': self.get_model_perm(Account, 'change'),
             'menus': (
                {'title': '用户管理', 'icon': 'fa fa-user'
                    , 'url': self.get_model_url(Account, 'changelist')},
                {'title': '部门管理', 'icon': 'fa fa-vimeo-square'
                    , 'url': self.get_model_url(Department, 'changelist')},
                {'title': '问题分类', 'icon': 'fa fa-vimeo-square'
                    , 'url': self.get_model_url(Category, 'changelist')},
                {'title': '工单类型', 'icon': 'fa fa-vimeo-square'
                    , 'url': self.get_model_url(TicketModel, 'changelist')},
                {'title': '工单列表', 'icon': 'fa fa-vimeo-square'
                    , 'url': self.get_model_url(Ticket, 'changelist')},
                {'title': '群组列表', 'icon': 'fa fa-vimeo-square'
                    , 'url': self.get_model_url(AccountGroup, 'changelist')},
            )},

        )

class AccountAdmin(object):
    list_display = ('nickname','user_id','status','desc'
                    ,'create_time','last_login',)

class AccountGroupAdmin(object):
    list_display = ('group_status','group_name','group_menu')

class DepartmentAdmin(object):
    list_display = ('partment_code','partment_desc','partment_lev',)

class CategoryAdmin(object):
    list_display = ('category_name','category_desc')

class TicketModelAdmin(object):
    list_display = ('ticket_id','ticket_title','ticket_model_desc',)


class TicketAdmin(object):
    list_display = ('ticket_id','ticket_title','ticket_desc','ticket_model_ticket',
                    'ticket_lev','ticket_listsort',)

class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True

xadmin.site.register(Department, DepartmentAdmin)
xadmin.site.register(Account, AccountAdmin)
xadmin.site.register(AccountGroup, AccountGroupAdmin)
xadmin.site.register(TicketModel, TicketModelAdmin)
xadmin.site.register(Category, CategoryAdmin)
xadmin.site.register(Ticket, TicketAdmin)



xadmin.site.register(xviews.BaseAdminView, BaseSetting)
xadmin.site.register(xviews.CommAdminView, GlobalSettings)



