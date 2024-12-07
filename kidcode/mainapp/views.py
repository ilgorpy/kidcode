from django.db import connection
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from users.models import User
from django.contrib import messages
from mainapp.models import *
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from .forms import  RecordForm, UserNameChangeForm, UserPasswordChangeForm, JournalForm, FieldsSettingsForm
from django.views.generic import UpdateView, CreateView, TemplateView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_http_methods
from mainapp.mixins import RoleRequiredMixin


@login_required
@require_POST
def update_grade(request):
    if 'grade_id' not in request.POST or 'new_grade' not in request.POST:
        return JsonResponse({'error': 'grade_id and new_grade are required'}, status=400)

    grade_id = request.POST.get('grade_id')
    new_grade = request.POST.get('new_grade')

    with connection.cursor() as cursor:
        try:
            cursor.execute("UPDATE mainapp_grade SET grade = %s WHERE id = %s", [new_grade, grade_id])
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        

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

class Journal(RoleRequiredMixin, TemplateView):
    form_class = JournalForm
    template_name = 'mainapp/journal.html'
    success_url = reverse_lazy("mainapp:journal")
    def get(self, request):
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
        
        return render(request,'mainapp/journal.html', {'journal_data': journal_data, 'form': form})
   

def index(request):
    return HttpResponse("Главная страница")


def constructor(request):
    return render(request, 'mainapp/constructor.html')


def profile(request):
    return render(request, 'mainapp/profile.html')

class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    template_name = "mainapp/profile.html"
    success_url = reverse_lazy("mainapp:profile")   
    def form_valid(self, form):
        messages.success(self.request, "Пароль успешно изменён!")
        return super().form_valid(form)

class UserNameChange(UpdateView):
    form_class = UserNameChangeForm
    success_url = reverse_lazy("mainapp:profile")
    template_name = "mainapp/profile.html"


class FieldsSettings(RoleRequiredMixin, CreateView):
    form_class = FieldsSettingsForm
    success_url = reverse_lazy("mainapp:constructor")
    template_name = "mainapp/constructor.html"
    


def task(request):
    return render(request, 'mainapp/task.html')