from django import forms
from django.contrib.auth import get_user_model
from mainapp.models import Task, Grade, Code


class JournalForm(forms.Form):
    status = forms.ChoiceField(choices=Grade.STATUS_CHOICES, label="Статус", widget=forms.Select)
    level = forms.ChoiceField(choices=[(t.level, t.level) for t in Task.objects.all().distinct('level')], label="Уровень", widget=forms.Select)
    name = forms.ChoiceField(choices=[(g.user.id, g.user.name) for g in Grade.objects.all().distinct('user')], 
                             label="Имя", widget=forms.Select)