from django.http import HttpResponse
from django.shortcuts import render
from mainapp.models import *


def journal(request):
    journal_data = list(JournalView.objects.all()) # используем кастомный менеджер
    return render(request, 'mainapp/journal.html', {'journal_data': journal_data})
   

def index(request):
    return HttpResponse("Главная страница")


def constructor(request):
    return render(request, 'mainapp/constructor.html')


def profile(request):
    return render(request, 'mainapp/profile.html')


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