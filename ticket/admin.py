from django.contrib import admin
from ticket.ticke_model.account import Account
from ticket.ticke_model.department import Department
# Register your models here.

admin.site.register(Account)
admin.site.register(Department)