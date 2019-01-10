# 引入我们创建的表单类
# coding:utf-8
from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse,JsonResponse
from django.views import View
from ticket.ticke_model.account import Account
from ticket.until import define, config
from ticket.ticket_form.account import LoginForm
from ticket.ticke_model.ticket import Ticket


class LoginView(View):
    def get(self, request):
        return render(request, 'ticket/login.html')

    def post(self, request):
        form = LoginForm(request.POST)  # form 包含提交的数据
        if form.is_valid():  # 如果提交的数据合法
            user_id = form.data['user_id']
            password = form.data['password']
            user = Account.objects.filter(user_id=user_id, password=password)
            if user:
                request.session["username"] = user[0].user_id
                return redirect("../../api/home/")
            else:
                # 用户不存在
                print('用户不存在')
                return JsonResponse({'error':'登录错误'})
        else:
            return redirect("../../api/login/")


def logout(request):
    request.session.clear()
    return redirect("../../api/login/")


def home(request):
    username_session = request.session.get("username")
    if username_session:
        user = Account.objects.get(user_id=username_session)
        if user.status == 0:
            return render(request, 'ticket/home.html', {'user': user,
                                                        'rootUrl': config.rootUrl,})
        else:
            actions_tickets = Ticket.objects.filter(ticket_listsort__user_id=request.session.get("username")).filter(
                ticket_status=0)
            done_tickets = Ticket.objects.filter(ticket_listsort__user_id=request.session.get("username")).filter(
                ticket_status=1)
            print(actions_tickets)
            print(done_tickets)
            return render(request, 'ticket/server.html', {'user': user,
                                                          'actions_tickets':actions_tickets,
                                                          'rootUrl': config.rootUrl,
                                                          'done_tickets':done_tickets})
    else:
        return redirect("../../api/login/")
