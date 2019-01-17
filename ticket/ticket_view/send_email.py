from django.core.mail import send_mail
from ticket.ticke_model.ticket import Ticket, TicketConfim
from ticket.ticke_model.account import Account


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
        send_mail('未完成工单提醒', '工单标题' + ticket.ticket_title + '   ' + '工单编号' + str(ticket.ticket_id),
                  'redbullticket@163.com',
                  senderuser, fail_silently=False)
    return


def sender():
    print("sdfsdfsf")


def my_scheduled_job():
    print('sdf')
    pass
