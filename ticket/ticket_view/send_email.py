from django.core.mail import send_mail
from ticket.ticke_model.ticket import Ticket, TicketConfim
from ticket.ticke_model.account import Account,AccountGroup
from datetime import date, time, datetime, timedelta
from django.http import HttpResponse, JsonResponse
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

# 开启定时工作
try:
    # 实例化调度器
    def my_job():
        sender_email()
        sender_admin_email()
        # 这里写你要执行的任务
        pass


    scheduler = BackgroundScheduler()
    # 调度器使用DjangoJobStore()
    # 另一种方式为每天固定时间执行任务，对应代码为：
    scheduler.add_job(my_job, 'cron', day_of_week='mon-fri', hour=17, minute=30, end_date='2099-05-30')
    # @register_job(scheduler, 'cron',day_of_week='mon,tue,wed,thu,fri,', hour='09', minute='55', second='00',id='task_time')
    scheduler.start()
except Exception as e:
    print(e)
    # 有错误就停止定时器
    scheduler.shutdown()


# 发送指定的工单
def sender_email_ticket(ticket):
    senderuser = []
    for confirm in ticket.ticket_listsort.filter(status=0):
        if confirm.user.email != None:
            senderuser.append(confirm.user.email)
    send_mail('未完成工单提醒', '工单标题' + ticket.ticket_title + '   ' + '工单编号' + str(ticket.ticket_id),
              'redbullticket@163.com',
              senderuser, fail_silently=False)
    return


# 根据数据库中所有未完成工单
def test_sender_email(request):
    all_ticket = Ticket.objects.filter(ticket_status=0)
    all_count = Account.objects.all()
    for acount in all_count:
        print(acount.email)
        if acount.email != None:
            strs = ''
            strs_confirm = ''
            tickets_confirm = all_ticket.filter(ticket_listsort__user=acount)
            tickets = all_ticket.filter(ticket_create_user=acount)
            if tickets.count() > 0:
                senderuser = [acount.email]
                for ticket in tickets:
                    strs = strs + '工单标题' + ticket.ticket_title + '   ' + '工单编号' + str(ticket.ticket_id) + '\n'
                try:
                    send_mail('未完成工单提醒', strs,
                      'redbullticket@163.com',
                      senderuser, fail_silently=False)
                except:
                    print('error')
            if tickets_confirm.count() > 0:
                senderuser = [acount.email]
                for ticket in tickets_confirm:
                    strs_confirm = strs_confirm + '工单标题' + ticket.ticket_title + '   ' + '工单编号' + str(ticket.ticket_id) + '\n'
                try:
                    send_mail('未完成工单提醒', strs_confirm,
                      'redbullticket@163.com',
                      senderuser, fail_silently=False)
                except:
                    print('error')
    return JsonResponse({'success':'e'})

# 根据数据库中所有未完成工单
def sender_email():
    all_ticket = Ticket.objects.filter(ticket_status=0)
    all_count = Account.objects.all()
    for acount in all_count:
        if acount.email != None:
            strs = ''
            strs_confirm = ''
            tickets_confirm = all_ticket.filter(ticket_listsort__user=acount)
            tickets = all_ticket.filter(ticket_create_user=acount)
            if tickets.count() > 0:
                senderuser = [acount.email]
                for ticket in tickets:
                    strs = strs + '工单标题' + ticket.ticket_title + '   ' + '工单编号' + str(ticket.ticket_id) + '\n'
                try:
                    send_mail('未完成工单提醒', strs,
                      'redbullticket@163.com',
                      senderuser, fail_silently=False)
                except:
                    print('error')
            if tickets_confirm.count() > 0:
                senderuser = [acount.email]
                for ticket in tickets_confirm:
                    strs_confirm = strs_confirm + '工单标题' + ticket.ticket_title + '   ' + '工单编号' + str(ticket.ticket_id) + '\n'
                try:
                    send_mail('未完成工单提醒', strs_confirm,
                      'redbullticket@163.com',
                      senderuser, fail_silently=False)
                except:
                    print('error')


# 根据数据库中所有未完成工单
def sender_admin_email():
    all_ticket = Ticket.objects.filter(ticket_status=0)
    all_group = AccountGroup.objects.all()
    group_status = []
    for group in all_group:
        if group.group_status in group_status:
            continue;
        else:
            group_status.append(group.group_status)
        strs = ''
        senderuser = []
        for user in Account.objects.filter(group__group_status=group.group_status).filter(group__group_menu='管理员'):
            senderuser.append(user.email)
        tickets = all_ticket.filter(ticket_create_user__group__group_status=group.group_status)
        for ticket in tickets:
            strs = strs + '工单标题' + ticket.ticket_title + '   ' + '工单编号' + str(ticket.ticket_id) + '\n'
        try:
            send_mail('未完成工单提醒', strs,
                      'redbullticket@163.com',
                      senderuser, fail_silently=False)
        except:
            print('error')
