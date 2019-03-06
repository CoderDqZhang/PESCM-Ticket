from django.core.mail import send_mail
from ticket.ticke_model.ticket import Ticket, TicketConfim
from ticket.ticke_model.account import Account
from datetime import date, time, datetime, timedelta
from django.http import HttpResponse, JsonResponse
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job


#开启定时工作
try:
    # 实例化调度器
    scheduler = BackgroundScheduler()
    # 调度器使用DjangoJobStore()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    # 设置定时任务，选择方式为interval，时间间隔为10s
    # 另一种方式为每天固定时间执行任务，对应代码为：
    # @register_job(scheduler, 'cron', day_of_week='mon-fri', hour='9', minute='30', second='10',id='task_time')
    @register_job(scheduler,"interval", seconds=10)
    def my_job():
        sender_email()
        # 这里写你要执行的任务
        pass
    register_events(scheduler)
    scheduler.start()
except Exception as e:
    print(e)
    # 有错误就停止定时器
    scheduler.shutdown()

def sender_email_ticket(ticket):
    senderuser = []
    for confirm in ticket.ticket_listsort.filter(status=0):
        if confirm.user.email != None:
            senderuser.append(confirm.user.email)
    send_mail('未完成工单提醒', '工单标题' + ticket.ticket_title + '   ' + '工单编号' + str(ticket.ticket_id),
              'redbullticket@163.com',
              senderuser, fail_silently=False)
    return


def sender_email():
    all_ticket = Ticket.objects.filter(ticket_status=0)
    for ticket in all_ticket:
        senderuser = []
        for confirm in ticket.ticket_listsort.filter(status=0):
            if confirm.user.email != None:
                senderuser.append(confirm.user.email)
        try:
            send_mail('未完成工单提醒', '工单标题' + ticket.ticket_title + '   ' + '工单编号' + str(ticket.ticket_id),
                  'redbullticket@163.com',
                  senderuser, fail_silently=False)
        except:
            print('error')
