# 引入我们创建的表单类
# coding:utf-8
from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse, JsonResponse
from django.views import View
from ticket.ticke_model.ticket import Ticket, TicketConfim
from ticket.ticke_model.account import Account
from ticket.ticke_model.category import Category, TicketModel
from ticket.ticke_model.department import Department
from ticket.ticket_view.send_email import sender_email_ticket
from ticket.ticket_form.ticket import TicketForm, TicketConfimForm
from ticket.until import define, config, serial_number
from django.forms.models import model_to_dict
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
import datetime


class TicketView(View):
    def get(self, request):
        username_session = request.session.get("username")
        if username_session:
            user = Account.objects.get(user_id=username_session)
            if request.GET.get('ticket_id') is not None:
                ticket = TicketModel.objects.get(ticket_id=request.GET.get('ticket_id'))
                departments = Department.objects.all()
                users = []
                if request.GET.get('department_code') is not None:
                    users = Account.objects.filter(department__partment_code=request.GET.get('department_code'))
                return render(request, 'ticket/ticket_create.html', {"ticket": ticket,
                                                                     "ticket_id": request.GET.get('ticket_id'),
                                                                     "category_id": request.GET.get('category_id'),
                                                                     'users': users,
                                                                     'user': user,
                                                                     'departments': departments,
                                                                     'rootUrl': config.rootUrl})
            elif request.GET.get('category_id') is not None:
                tickets = TicketModel.objects.filter(ticket_model=request.GET.get('category_id'))
                return render(request, 'ticket/ticket_create.html', {"tickets": tickets,
                                                                     'category_id': request.GET.get('category_id'),
                                                                     'user': user,
                                                                     'rootUrl': config.rootUrl
                                                                     })
            else:
                catgorys = Category.objects.all()
                return render(request, 'ticket/ticket_create.html', {"catgorys": catgorys,
                                                                     'user': user,
                                                                     'rootUrl': config.rootUrl})
        else:
            return redirect("../../../api/login/")

    def post(self, request):
        username_session = request.session.get("username")
        if username_session:
            tickt_form = TicketForm(request.POST)
            ticketModel = TicketModel.objects.get(ticket_id=request.GET.get('ticket_id'))
            ticketModel.ticket_model = Category.objects.get(category_id=request.GET.get('category_id'))
            user = Account.objects.get(user_id=username_session)
            if tickt_form.is_valid():
                try:
                    tickt_form.data['check_box']
                    isCheckForm = 1  # 为紧急状态
                except:
                    isCheckForm = 0

                ticket_id = serial_number.get_ticket_id(ticketModel)
                ticket = Ticket.objects.create(
                    ticket_show_id = ticket_id,
                    ticket_title=tickt_form.data['ticket_title'],
                    ticket_desc=tickt_form.data['ticket_desc'],
                    ticket_lev=isCheckForm,
                    dev_push_time=tickt_form.data['dev_push_time'],
                    pub_push_time=tickt_form.data['pub_push_time'],
                    ticket_remark=tickt_form.data['ticket_remark'],
                    handel_time=tickt_form.data['handel_time'],
                    ticket_create_user=user,
                    ticket_model_ticket=ticketModel
                )

                try:
                    ticket.ticket_file = request.FILES.get('file_data', None)
                    ticket.file_name = str(request.FILES.get('file_data', None))
                except:
                    ticket.ticket_file = None

                for model in tickt_form.cleaned_data["ticket_listsort"]:
                    ticket_confim = TicketConfim.objects.create(
                        user=model
                    )
                    ticket.ticket_listsort.add(ticket_confim)
                ticket.save()
                sender_email_ticket(ticket)
                url = "../../../api/ticket/detail/?ticket_id=" + str(ticket.ticket_id)
                return redirect(url)
            else:
                return render(request, 'ticket/myticket/my_ticket.html')
        else:
            return redirect("../../../api/login/")


class MyticketView(View):
    def get(self, request):
        username_session = request.session.get("username")
        if username_session:
            user = Account.objects.get(user_id=username_session)
            if user.status == 1:
                myticket = Ticket.objects.get_queryset().filter(
                    ticket_listsort__user__user_id__exact=username_session).order_by(
                    '-create_time')
                for ticket in myticket:
                    ticket.ticket_status = ticket.ticket_listsort.get(user__user_id=username_session).status
            else:
                myticket = Ticket.objects.get_queryset().filter(ticket_create_user__user_id=username_session).order_by(
                    '-create_time')
            if request.GET.get('dateType') is not None:
                dateType = int(request.GET.get('dateType'))
                now = timezone.now()
                yeastoday = now - datetime.timedelta(days=1)
                yeastoday1 = now - datetime.timedelta(days=2)
                week = now - datetime.timedelta(days=7)
                if int(request.GET.get('dateType')) == 1:
                    myticket = myticket.filter(create_time__gt=yeastoday)
                elif int(request.GET.get('dateType')) == -1:
                    myticket = myticket.filter(create_time__range=(yeastoday, yeastoday1))
                elif int(request.GET.get('dateType')) == -7:
                    myticket = myticket.filter(create_time__gt=week)
            else:
                dateType = 100

            if request.GET.get('status') is not None:
                status = int(request.GET.get('status'))
                if int(request.GET.get('status')) != 4:
                    myticket = myticket.filter(ticket_status=request.GET.get('status'))
            else:
                status = 4

            myticket_list = myticket
            paginator = Paginator(myticket, 10)
            # 分页控制

            if request.GET.get('page') != None:
                page = int(request.GET.get('page'))

            # 当前分页
            try:
                myticket_list = paginator.page(page)  # 获取当前页码的记录
            except PageNotAnInteger:
                myticket_list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
            except EmptyPage:
                myticket_list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容

            if myticket_list.__len__() == 0:
                page = 0

            return render(request, 'ticket/myticket/my_ticket.html', {'myticket_list': myticket_list,
                                                                      'page': paginator,
                                                                      'status': status,
                                                                      'dateType': dateType,
                                                                      'rootUrl': config.rootUrl,
                                                                      'user': user
                                                                      })
        else:
            return redirect("../../../api/login/")

    def post(self, request):
        return redirect("../../../api/login/")

    def has_nex_pre(blog_id):
        has_prev = False
        has_next = False
        id_prev = id_next = int(blog_id)
        blog_id_max = Ticket.objects.all().order_by('-id').first()
        id_max = blog_id_max.id
        while not has_prev and id_prev >= 1:
            blog_prev = Ticket.objects.filter(id=id_prev - 1).first()
            if not blog_prev:
                id_prev -= 1
            else:
                has_prev = True
        while not has_next and id_next <= id_max:
            blog_next = Ticket.objects.filter(id=id_next + 1).first()
            if not blog_next:
                id_next += 1
            else:
                has_next = True

        data = {}
        data['blog_prev'] = blog_prev
        data['blog_next'] = blog_next
        data['has_next'] = has_next
        data['has_prev'] = has_prev
        # 将状态码与上下博客传递给前端页面
        return data


class TicketListView(View):
    def get(self, request):
        username_session = request.session.get("username")
        if username_session:
            user = Account.objects.get(user_id=username_session)
            ticket = Ticket.objects.all().order_by(
                '-create_time')
            if user.status == 1:
                for ticket1 in ticket:
                    if ticket1.ticket_listsort.filter(user__user_id=username_session).count() == 1:
                        ticket1.ticket_status = ticket1.ticket_listsort.get(user__user_id=username_session).status

            if request.GET.get('dateType') is not None:
                dateType = int(request.GET.get('dateType'))
                now = timezone.now()
                yeastoday = now - datetime.timedelta(days=1)
                yeastoday1 = now - datetime.timedelta(days=2)
                week = now - datetime.timedelta(days=7)
                if int(request.GET.get('dateType')) == 1:
                    ticket = ticket.filter(create_time__gt=yeastoday)
                elif int(request.GET.get('dateType')) == -1:
                    ticket = ticket.filter(create_time__range=(yeastoday, yeastoday1))
                elif int(request.GET.get('dateType')) == -7:
                    ticket = ticket.filter(create_time__lt=week)
            else:
                dateType = 100

            if request.GET.get('status') is not None:
                status = int(request.GET.get('status'))
                if int(request.GET.get('status')) != 4:
                    ticket = ticket.filter(ticket_status=request.GET.get('status'))
            else:
                status = 4

            paginator = Paginator(ticket, 10)
            # 分页控制

            if request.GET.get('page') != None:
                page = int(request.GET.get('page'))

            # 当前分页
            try:
                ticket_list = paginator.page(page)  # 获取当前页码的记录
            except PageNotAnInteger:
                ticket_list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
            except EmptyPage:
                ticket_list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容

            if ticket_list.__len__() == 0:
                page = 0

            return render(request, 'ticket/ticketlist/ticket_list.html', {'ticket_list': ticket_list,
                                                                          'page': paginator,
                                                                          'status': status,
                                                                          'dateType': dateType,
                                                                          'rootUrl': config.rootUrl,
                                                                          'user': user
                                                                          })
        else:
            return redirect("../../../api/login/")

    def post(self, request):
        return HttpResponse({"": ""})


class TicketDetailView(View):
    def get(self, request):
        username_session = request.session.get("username")
        if username_session:
            user = Account.objects.get(user_id=username_session)
            try:
                try:
                    ticket = Ticket.objects.get(ticket_show_id=request.GET.get('ticket_id'))
                except Ticket.DoesNotExist:
                    ticket = Ticket.objects.get(ticket_id=request.GET.get('ticket_id'))
                if ticket.ticket_listsort.filter(user__user_id=username_session):
                    return render(request, 'ticket/server_ticket_detail.html', {'ticket': ticket,
                                                                                'confirms': ticket.ticket_listsort.all(),
                                                                                'rootUrl': config.rootUrl,
                                                                                'user': user
                                                                                })
                return render(request, 'ticket/ticket_detail.html', {'ticket': ticket,
                                                                     'confirms': ticket.ticket_listsort.all(),
                                                                     'rootUrl': config.rootUrl,
                                                                     'user': user
                                                                     })
            except Ticket.DoesNotExist:
                return JsonResponse({'error': '数据出错'})
        else:
            return redirect("../../../api/login/")


class TicketServerDetailView(View):
    def get(self, request):
        username_session = request.session.get("username")
        if username_session:
            user = Account.objects.get(user_id=username_session)
            ticket = Ticket.objects.get(ticket_id=request.GET.get('ticket_id'))
            departments = Department.objects.all()
            users = []
            if request.GET.get('department_code') is not None:
                users = Account.objects.filter(department__partment_code=request.GET.get('department_code'))
            return render(request, 'ticket/server_ticket_detail.html', {'ticket': ticket,
                                                                        'confirms': ticket.ticket_listsort.all(),
                                                                        'rootUrl': config.rootUrl,
                                                                        'user': user,
                                                                        'departments': departments,
                                                                        'users': users
                                                                        })
        else:
            return redirect("../../../api/login/")

    def post(self, request):
        username_session = request.session.get("username")
        if username_session:
            user = Account.objects.get(user_id=username_session)
            tickt_form = TicketConfimForm(request.POST, )
            ticket = Ticket.objects.get(ticket_id=request.GET.get('ticket_id'))

            departments = Department.objects.all()
            users = []
            if request.GET.get('department_code') is not None:
                users = Account.objects.filter(department__partment_code=request.GET.get('department_code'))

            isCheckForm = True
            try:
                tickt_form.data['check_box']
                isCheckForm = False
            except:
                isCheckForm = True

            if tickt_form.is_valid() | isCheckForm:
                ticket_confirm = ticket.ticket_listsort.get(user__user_id=request.session.get("username"))
                try:
                    ticket_confirm.confirm_file = request.FILES.get('file_data', None)
                    ticket_confirm.file_name = str(request.FILES.get('file_data'))
                except:
                    ticket_confirm.confirm_file = None

                ticket_confirm.status = 1
                ticket_confirm.content = tickt_form.data['ticket_content']
                ticket_confirm.confirm_remark = tickt_form.data['confirm_remark']
                ticket_confirm.confirm_time = timezone.now()

                try:
                    # 根据是否选中checkbox来选择转派人员
                    tickt_form.data['check_box']

                    # 处理完成后转派给他人
                    ticket_confirm.transfer = 1

                    for model in tickt_form.cleaned_data["ticket_listsort"]:
                        if ticket.ticket_listsort.filter(user__user_id=model.user_id):
                            ticket_confim = TicketConfim.objects.create(
                                user=model,
                                transfer=2,
                            )
                            ticket.ticket_listsort.add(ticket_confim)

                except:
                    if ticket.ticket_listsort.filter(status=0).count() == 0:
                        ticket.ticket_status = 3

                ticket_confirm.save()
                ticket.save()
                return render(request, 'ticket/server_ticket_detail.html', {'ticket': ticket,
                                                                            'confirms': ticket.ticket_listsort.all(),
                                                                            'rootUrl': config.rootUrl,
                                                                            'user': user,
                                                                            'departments': departments,
                                                                            'users': users
                                                                            })
            else:
                return render(request, 'ticket/server_ticket_detail.html', {'ticket': ticket,
                                                                            'confirms': ticket.ticket_listsort.all(),
                                                                            'rootUrl': config.rootUrl,
                                                                            'user': user,
                                                                            'departments': departments,
                                                                            'users': users
                                                                            })
        else:
            return redirect("../../../api/login/")


def test(request):
    return render(request, 'ticket/test.html')


def get_department_user(request):
    users = Account.objects.filter(department__partment_code=request.GET.get('department_code'))
    jsonData = []
    for user in users:
        jsonData.append(model_to_dict(user, exclude=['avatar']))
    return JsonResponse({"user_list": jsonData})
