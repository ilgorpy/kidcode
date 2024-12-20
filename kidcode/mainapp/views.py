from django.db import connection
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404

from django.db.models import Q
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import View,UpdateView, TemplateView

import json
from .forms import *
from mainapp.models import *
from mainapp.mixins import RoleRequiredMixin


class Task1(View):
    model = Task
    form_class = TaskTextForm
    template_name = 'mainapp/task.html'
    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        return render(request, 'mainapp/task.html', {'task': task})


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
    return redirect('users/login')


class UserProfileChangeView(View):
    form_class = UserProfileChangeForm
    template_name = "mainapp/profile.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # Смена имени
            name = form.cleaned_data.get('name')
            if name:
                request.user.name = name  # или request.user.first_name/last_name в зависимости от ваших требований
                request.user.save()
                messages.success(request, "Имя успешно изменено!")

            # Смена пароля
            new_password1 = form.cleaned_data.get('new_password1')
            new_password2 = form.cleaned_data.get('new_password2')
            if new_password1:  # Проверяем только если новое имя пароля заполнено
                if new_password1 == new_password2:
                    request.user.set_password(new_password1)
                    request.user.save()
                    messages.success(request, "Пароль успешно изменён!")
                else:
                    messages.error(request, "Пароли не совпадают!")

            return redirect('mainapp:profile')

        return render(request, self.template_name, {'form': form})

class FieldsSettings(View):
    template_name = 'mainapp/constructor.html'
    model = Task
    fields = []

    def get(self, request, *args, **kwargs):
        fields_form = FieldsSettingsForm()
        task_form = TaskTextForm()
        return render(request, self.template_name, {
            'fields_form': fields_form,
            'task_form': task_form
        })

    def post(self, request, *args, **kwargs):
            data = json.loads(request.body)  # Загружаем данные из JSON
            fields_form = FieldSaveForm(data)
            task_form = TaskTextForm(data)
         
            if fields_form.is_valid() and task_form.is_valid():
                game_field = fields_form.save()
                task = task_form.save(commit=False)
                task.gamefield = game_field
                task.save()
                return JsonResponse({'status': 'success'})  # Возвращаем JSON-ответ

            return JsonResponse({'status': 'errorrrr', 'errors': fields_form.errors}, status=400)



def get_chapters(request):
    chapters = Task.objects.values('chapter').distinct()
    chapter_list = [chapter['chapter'] for chapter in chapters]
    print(chapter_list)
    return JsonResponse(chapter_list, safe=False)

def get_levels(request, chapter_name):
    levels = Task.objects.filter(chapter=chapter_name).values('level')
    task_id = Task.objects.filter(chapter=chapter_name).values('id')
    task_id_list = [task['id'] for task in task_id]
    level_list = [level['level'] for level in levels]
    result = dict(zip(task_id_list, level_list))
    print(result)
    return JsonResponse(result, safe=False)


    

    