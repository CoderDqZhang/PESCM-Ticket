# 引入我们创建的表单类
# coding:utf-8
from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse, JsonResponse
from django.views import View
from ticket.ticke_model.account import Account
from ticket.until import define, config
from ticket.ticket_form.account import LoginForm,ChangePasswordForm
from ticket.ticke_model.ticket import Ticket
from django.forms.models import model_to_dict
from django.db.models import Q

#登录界面
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
                return JsonResponse({'error': '登录错误'})
        else:
            return redirect("../../api/login/")

#修改密码
class ChangePasswordView(View):
    def get(self, request):
        return render(request, 'ticket/change_password.html')

    def post(self, request):
        form = LoginForm(request.POST)  # form 包含提交的数据
        username_session = request.session.get("username")
        if username_session:
            password = form.data['old_password']
            user = Account.objects.filter(user_id=username_session, password=password)
            if user.count() > 0:
                user[0].password = form.data['new_password']
                user[0].save()
                return JsonResponse({'success': '修改密码成功'})
            else:
                # 用户不存在
                print('用户不存在')
                return JsonResponse({'error': '原密码错误'})
        else:
            return render(request, 'ticket/login.html')

# 修改邮箱
class ChangeEmailView(View):
    def get(self, request):
        username_session = request.session.get("username")
        user = Account.objects.get(user_id=username_session)
        return render(request, 'ticket/change_email.html',context={'user':user})

    def post(self, request):
        form = LoginForm(request.POST)  # form 包含提交的数据
        username_session = request.session.get("username")
        if username_session:
            email = form.data['email']
            user = Account.objects.get(user_id=username_session)
            if user:
                user.email = form.data['email']
                user.save()
                return JsonResponse({'success': '修改邮箱成功'})
            else:
                # 用户不存在
                print('用户不存在')
                return JsonResponse({'error': '修改邮箱错误'})
        else:
            return render(request, 'ticket/change_email.html')

#登出
def logout(request):
    request.session.clear()
    return redirect("../../api/login/")

#首页请求
def home(request):
    username_session = request.session.get("username")
    if username_session:
        user = Account.objects.get(user_id=username_session)
        #根据甲乙方加载不同请求界面
        if user.status == 0:
            #未完成工单
            actions_tickets = Ticket.objects.filter(Q(ticket_listsort__status=0) &
                                                    Q(ticket_create_user=request.session.get("username"))).\
                exclude(ticket_status=3).distinct().order_by("-create_time")[:10]
            #待审核工单
            todo_actions_tickets = Ticket.objects.filter(Q(ticket_listsort__status=1) &
                                                         Q(ticket_create_user=request.session.get("username")) &
                                                         Q(ticket_listsort__check=0)).\
                exclude(ticket_status=3).distinct().order_by("-create_time")[:10]
            #待部署工单
            todo_pubtime_tickets = Ticket.objects.filter(Q(ticket_listsort__status=1) &
                                                         Q(ticket_create_user=request.session.get("username")) &
                                                         Q(ticket_listsort__check=1)).\
                exclude(ticket_status=3).distinct().order_by("-create_time")[:10]
            #已完成工单
            done_tickets = Ticket.objects.filter(
                ticket_create_user=request.session.get("username")).filter(
                ticket_status=3).order_by("-create_time")[:10]

            return render(request, 'ticket/home.html', {'user': user,
                                                        'actions_tickets': actions_tickets,
                                                        'done_tickets': done_tickets,
                                                        'todo_actions_tickets': todo_actions_tickets,
                                                        'todo_pubtime_tickets':todo_pubtime_tickets,
                                                        'rootUrl': config.rootUrl, })
        else:
            # 未完成工单
            actions_tickets = Ticket.objects.filter(
                ticket_listsort__user__user_id__exact=request.session.get("username")).filter(
                ticket_status=0).order_by("-create_time")[:10]
            # 待审核工单
            todo_actions_tickets = Ticket.objects.filter(Q(ticket_listsort__status=1) &
                                                         Q(ticket_listsort__user__user_id__exact=request.session.get("username")) &
                                                         Q(ticket_listsort__check=0)). \
                                       exclude(ticket_status=3).distinct().order_by("-create_time")[:10]
            # 待部署工单
            todo_pubtime_tickets = Ticket.objects.filter(Q(ticket_listsort__status=1) &
                                                         Q(ticket_listsort__user__user_id__exact=request.session.get("username")) &
                                                         Q(ticket_listsort__check=1)). \
                                       exclude(ticket_status=3).distinct().order_by("-create_time")[:10]
            # 已完成工单
            done_tickets = Ticket.objects.filter(
                ticket_listsort__user__user_id__exact=request.session.get("username")).filter(
                ticket_status=3).order_by("-create_time")[:10]

            return render(request, 'ticket/server.html', {'user': user,
                                                          'actions_tickets': actions_tickets,
                                                          'rootUrl': config.rootUrl,
                                                          'done_tickets': done_tickets,
                                                          'todo_pubtime_tickets': todo_pubtime_tickets,
                                                          'todo_actions_tickets':todo_actions_tickets})
    else:
        return redirect("../../api/login/")



def home_api(request):

    actions_tickets = Ticket.objects.filter(
        ticket_listsort__user__user_id__exact=request.session.get("username")).filter(
        ticket_status=0).order_by("-create_time")
    jsonData = []

    for actions_ticket in actions_tickets:
        jsonData.append(model_to_dict(actions_ticket, exclude=['ticket_file','ticket_listsort']))
    return JsonResponse({"actions_tickets": jsonData})



