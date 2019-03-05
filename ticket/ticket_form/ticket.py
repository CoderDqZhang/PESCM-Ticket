from django import forms
from ticket.ticke_model.account import Account
from ticket.ticke_model.category import TicketModel

class TicketForm(forms.Form):
    ticket_title = forms.TextInput()
    ticket_desc = forms.Textarea()
    check_box = forms.CheckboxInput()
    ticket_lev = forms.CheckboxInput()  # 状态，一般，紧急，
    ticket_listsort = forms.ModelMultipleChoiceField(queryset=Account.objects.all())
    handel_time = forms.FloatField()
    ticket_remark = forms.Textarea()

class TicketConfimForm(forms.Form):
    ticket_content = forms.Textarea()
    check_box = forms.CheckboxInput()
    dev_push_time = forms.TextInput()
    pub_push_time = forms.TextInput()
    handel_time = forms.FloatField()
    confirm_remark = forms.Textarea()

class TicketConfirmForm(forms.Form):
    ticket_listsort = forms.ModelMultipleChoiceField(queryset=Account.objects.all())

class ChangeTimeForm(forms.Form):
    handel_time = forms.FloatField()


class TicketCheckForm(forms.Form):
    ticket_id = forms.CharField()

