import sys
from django.views.debug import technical_500_response
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse, JsonResponse

#中间件检测用户是否登录
class UserSessionMiddleware(MiddlewareMixin):
    def process_request(self,request):
        parpam = str(request.get_full_path()).split('/')
        if request.session.get("username") == None \
                and request.get_full_path() != '/api/login/' \
                and 'admin' not in parpam \
                and 'xadmin' not in parpam:
            return redirect("../../api/login/")


class UserBasedExceptionMiddleware(object):
    def process_exception(self, request, exception):
        if request.user.is_superuser or request.META.get('REMOTE_ADDR') in settings.INTERNAL_IPS:
            return technical_500_response(request, *sys.exc_info())