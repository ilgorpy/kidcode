from django.http import HttpResponse
from django.shortcuts import render



def index(request):
    return HttpResponse("Главная страница")


def constructor(request):
    return render(request, 'mainapp/constructor.html')


def profile(request):
    return render(request, 'mainapp/profile.html')


def journal(request):
    return render(request, 'mainapp/journal.html')


def record(request):
    return render(request, 'mainapp/record.html')


def task(request):
    return render(request, 'mainapp/task.html')