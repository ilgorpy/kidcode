from django import forms
from django.contrib.auth import get_user_model
from mainapp.models import Task, Grade, Code
from django.contrib.auth.forms import SetPasswordForm


class JournalForm(forms.Form):
    status = forms.ChoiceField(choices=Grade.STATUS_CHOICES, label="Статус", widget=forms.Select, required=False)
    level = forms.CharField(label="Уровень", widget = forms.TextInput(attrs={'class': 'form-input'}), required=False)
    name = forms.CharField(label="Имя", widget = forms.TextInput(attrs={'class': 'form-input'}), required=False)

class RecordForm(forms.Form):
    grade = forms.ChoiceField(choices=Grade.GRADES, label="Оценка", widget=forms.Select, required=False)
    level = forms.CharField(label="Уровень", widget = forms.TextInput(attrs={'class': 'form-input'}), required=False)


class UserNameChangeForm(forms.Form):
    name = forms.CharField(label="Имя", widget = forms.TextInput(attrs={'class': 'form-input'}), required=False)

class UserPasswordChangeForm(SetPasswordForm):
    new_password1 = forms.CharField(label="Новый пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput(attrs={'class': 'form-input'}))