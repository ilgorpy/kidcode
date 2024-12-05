from django.http import HttpResponse
from django.shortcuts import render
from users.models import User
from mainapp.models import *
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from .forms import  RecordForm, UserNameChangeForm, UserPasswordChangeForm, JournalForm
from django.views.generic import UpdateView
from django.contrib.auth.views import PasswordChangeView


def record(request):
    record_data = []
    form = RecordForm(request.GET)
    user_id = request.user.id
    filters = Q(user_id=user_id)

    if form.is_valid():
        grade = form.cleaned_data.get('grade')
        level = form.cleaned_data.get('level')

        if grade:
            filters &= Q(grade=grade)
        if level:
            filters &= Q(level=level)

        record_data = list(RecordView.objects.filter(filters))

    else:
        record_data = list(RecordView.objects.filter(filters))
    
    return render(request, 'mainapp/record.html', {'record_data': record_data, 'form': form})


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

class UserNameChange(UpdateView):
    form_class = UserNameChangeForm
    success_url = reverse_lazy("mainapp:profile")
    template_name = "mainapp/profile.html"


def task(request):
    return render(request, 'mainapp/task.html')