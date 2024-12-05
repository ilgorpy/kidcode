from django.http import HttpResponse
from django.shortcuts import render
from users.models import User
from mainapp.forms import JournalForm
from mainapp.models import *
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from .forms import  UserPasswordChangeForm
from django.contrib.auth.views import PasswordChangeView



def journal(request):
    journal_data = []
    form = JournalForm(request.GET)

    if form.is_valid():
        status = form.cleaned_data.get('status')
        level = form.cleaned_data.get('level')
        user_name = form.cleaned_data.get('name')

        filters = Q()
        if status:
            filters &= Q(status=status)
        if level:
            filters &= Q(level=level)
        if user_name:
            filters &= Q(name__iexact=user_name)

        journal_data = list(JournalView.objects.filter(filters))

    else:
        journal_data = list(JournalView.objects.all())
        
    return render(request, 'mainapp/journal.html', {'journal_data': journal_data, 'form': form})
   

def index(request):
    return HttpResponse("Главная страница")


def constructor(request):
    return render(request, 'mainapp/constructor.html')


def profile(request):
    return render(request, 'mainapp/profile.html')

class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("users:password_change_done")
    template_name = "mainapp/profile.html"


# def journal(request):
#     data = {
#         'name': [],
#         'task_id': [],
#         'level': [],
#         'submission_date': [],
#         'status': [],
#         'grade': [],
#         'code': [],
#     }

#     grades = Grade.objects.select_related('task', 'code', 'user')

#     for grade in grades:
#         data['name'].append(grade.user.name)
#         data['task_id'].append(grade.task.id)
#         data['level'].append(grade.task.level)
#         data['submission_date'].append(grade.submission_date)
#         data['status'].append(grade.status)
#         data['grade'].append(grade.grade)
#         data['code'].append(grade.code.code)

#     return render(request, 'mainapp/journal.html')


def record(request):
    return render(request, 'mainapp/record.html')


def task(request):
    return render(request, 'mainapp/task.html')