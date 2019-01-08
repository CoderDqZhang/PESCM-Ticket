from django.conf.urls import url, include
from rest_framework import routers
from ticket.ticket_view import account,department,ticket


# router = routers.DefaultRouter()
# router.register(r'users', account.UserViewSet)
# router.register(r'groups', account.GroupViewSet)

urlpatterns = [
    url(r'^login/$', account.LoginView.as_view()),
    url(r'^home/$', account.home),
    url(r'^logout/$', account.logout),


    url(r'^ticket/create/$', ticket.TicketView.as_view()),
    url(r'^ticket/myticket/$', ticket.MyticketView.as_view()),
    url(r'^ticket/list/$', ticket.TicketListView.as_view()),

    url(r'^ticket/detail/$', ticket.TicketDetailView.as_view()),
    url(r'^ticket/server/detail/$', ticket.TicketServerDetailView.as_view()),

    url(r'^ticket/create/department/user/', ticket.get_department_user)
]