from django import forms
from django.contrib.auth import get_user_model
from mainapp.models import Task, Grade, Code


class JournalForm(forms.Form):
    status = forms.ChoiceField(choices=get_user_model().GRADE_STATUS, label='Статус')