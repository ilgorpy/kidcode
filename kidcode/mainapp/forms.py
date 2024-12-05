from django import forms
from django.contrib.auth import get_user_model
from mainapp.models import Task, Grade, Code
from django.contrib.auth.forms import SetPasswordForm


class JournalForm(forms.Form):
    status = forms.ChoiceField(choices=Grade.STATUS_CHOICES, label="Статус", widget=forms.Select)
    level = forms.CharField( label="Уровень", widget = forms.TextInput(attrs={'class': 'form-input'}))
    name = forms.CharField(label="Имя", widget = forms.TextInput(attrs={'class': 'form-input'}))

class UserPasswordChangeForm(SetPasswordForm):
    new_password1 = forms.CharField(label="Новый пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput(attrs={'class': 'form-input'}))