from django import forms
from ticket.ticke_model.account import Account
from ticket.ticke_model.category import TicketModel

class TicketForm(forms.Form):
    ticket_title = forms.TextInput()
    ticket_desc = forms.Textarea()
    ticket_lev = forms.CheckboxInput()  # 状态，一般，紧急，
    ticket_listsort = forms.ModelMultipleChoiceField(queryset=Account.objects.all())



class TicketConfimForm(forms.Form):
    ticket_content = forms.Textarea()
    check_box = forms.CheckboxInput()
    ticket_listsort = forms.ModelMultipleChoiceField(queryset=Account.objects.all())
    # file_data = forms.FileField()
