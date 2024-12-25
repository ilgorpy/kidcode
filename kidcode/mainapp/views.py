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
from django.views.decorators.csrf import csrf_exempt
import json
from .forms import *
from mainapp.models import *
from mainapp.mixins import RoleRequiredMixin
from users.models import User

from RestrictedPython import compile_restricted, safe_globals, utility_builtins

class Task1(View):
    template_name = 'mainapp/task.html'

    def get(self, request, pk):
        if request.path.endswith('/data/'):
            return self.get_game_field_data(request, pk)
        elif request.path.endswith('/clue/'):
            return self.get_clue(request, pk)
        elif request.path.endswith('/position/'):
            return self.get_player_position(request, pk, request.user.id)
        else:
            return self.get_task_view(request, pk)
        
    def post(self, request, pk, user_id):
        if 'reset' in request.path:
            return self.post_reset(request, pk, user_id)
        else:
            return self.post_move_player(request, pk, user_id)

    def get_task_view(self, request, pk):
    # Загрузка задачи
        task = get_object_or_404(Task, pk=pk)

        # Используем связь task.gamefield_id для получения игрового поля
        game_field = get_object_or_404(GameField, id=task.gamefield_id)

        # Инициализация начальных координат игрока по умолчанию
        initial_x, initial_y = 0, 0

        # Попытка найти игрока в данных игрового поля
        try:
            game_field_data = game_field.data  # Предполагается, что это уже список
            if isinstance(game_field_data, str):
                game_field_data = json.loads(game_field_data)  # Преобразование из строки JSON, если это строка
            player_data = next((item for item in game_field_data if item.get('id') == 'player'), None)
            if player_data:
                initial_x = player_data.get('x', 0)
                initial_y = player_data.get('y', 0)
        except Exception as e:
            print(f"Ошибка при обработке данных игрового поля: {e}")

        # Проверяем, существует ли Player для данного пользователя и игрового поля
        player, created = Player.objects.get_or_create(
            user=request.user,
            game_field=game_field,
            defaults={'x': initial_x, 'y': initial_y}  # Используем извлеченные координаты
        )

        if created:
            print(f"Создан новый игрок для пользователя {request.user.id} и игрового поля {game_field.id} с координатами ({initial_x}, {initial_y})")

        # Извлекаем код из базы данных, если он существует
        try:
            code_entry = Code.objects.get(user=request.user, game_field=game_field)
            user_code = code_entry.code  # Получаем код
        except Code.DoesNotExist:
            user_code = ""  # Если кода нет, пустое значение

        # Передаем данные в контекст
        context = {
            'task': task,
            'game_field': game_field,
            'player': player,
            'user_code': user_code,  # Добавляем код в контекст
        }
        return render(request, self.template_name, context)




    def get_game_field_data(self, request, pk):
        """
        Обработка AJAX-запросов для получения данных игрового поля.
        """
        # Загружаем данные задачи
        task = get_object_or_404(Task, pk=pk)

        # Используем связь task.gamefield_id для получения игрового поля
        game_field = get_object_or_404(GameField, id=task.gamefield_id)

        # Формируем JSON-ответ
        return JsonResponse({
            'data': game_field.data,
            'width': game_field.width,
            'height': game_field.height,
        })
    
    def get_clue(self, request, pk):
        """
        Возвращает подсказку задачи в формате JSON.
        """
        task = get_object_or_404(Task, pk=pk)
        return JsonResponse({'clue': task.clue})
    
    def get_player_position(request, pk, user_id):
        try:
            player = Player.objects.get(user_id=user_id)
            return JsonResponse({"x": player.x, "y": player.y})
        except Player.DoesNotExist:
            return JsonResponse({"error": "Player not found"}, status=404)

    def post_move_player(self, request, pk, user_id):
        print(f"Task ID: {pk}, Player ID: {user_id}")
        print(f"Request Body: {request.body.decode('utf-8')}")

        # Получаем задачу и игровое поле
        try:
            task = get_object_or_404(Task, pk=pk)
            game_field = get_object_or_404(GameField, id=task.gamefield_id)
        except Exception as e:
            print(f"Error fetching task or game field: {e}")
            return JsonResponse({"error": "Task or game field not found"}, status=404)

        # Пытаемся получить игрока
        try:
            player = Player.objects.get(user_id=user_id, game_field=game_field)
        except Player.DoesNotExist:
            return JsonResponse({"error": "Player not found"}, status=404)

        # Получаем и проверяем пользовательский код
        try:
            data = json.loads(request.body)
            user_code = data.get('code', '')
            print(f"Received code: {user_code}")
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            return JsonResponse({"error": "Некорректный формат данных JSON"}, status=400)

        if not user_code:
            print("Code is empty")
            return JsonResponse({"error": "Код не предоставлен"}, status=400)

        # Сохраняем код в базу данных
        try:
            code_entry, created = Code.objects.update_or_create(
                user_id=user_id, game_field=game_field,
                defaults={'code': user_code}
            )
            if created:
                print(f"Создана новая запись кода для пользователя {user_id} на игровом поле {game_field.id}")
            else:
                print(f"Обновлена запись кода для пользователя {user_id} на игровом поле {game_field.id}")
        except Exception as e:
            print(f"Error saving code: {e}")
            return JsonResponse({"error": "Ошибка при сохранении кода"}, status=500)

        # Настраиваем безопасные переменные для исполнения кода
        safe_globals = {
            "_getiter_": iter,
            **utility_builtins,
        }

        safe_locals = {
            "move_down": lambda: self.move_player(player, 0, 64, game_field),
            "move_up": lambda: self.move_player(player, 0, -64, game_field),
            "move_left": lambda: self.move_player(player, -64, 0, game_field),
            "move_right": lambda: self.move_player(player, 64, 0, game_field),
            "range": range,
        }

        # Исполнение пользовательского кода
        try:
            byte_code = compile_restricted(user_code, '<inline>', 'exec')
            print(f"Executing user code: {user_code}")
            print(f"Safe locals before execution: {safe_locals.keys()}")
            exec(byte_code, {**safe_globals, **utility_builtins}, safe_locals)
            player.refresh_from_db()  # Убедимся, что данные обновились
        except Exception as e:
            print(f"Ошибка выполнения кода: {e}")
            return JsonResponse({"error": str(e)}, status=400)

        # Проверка достижения цели (goal)
        level_completed = False
        for obj in game_field.data:
            if obj["x"] == player.x and obj["y"] == player.y and obj["id"] == "goal":
                print("Player reached the goal!")
                level_completed = True
                break

        response_data = {
            "x": player.x,
            "y": player.y,
            "level_completed": level_completed,
        }

        if level_completed:
            response_data["message"] = "Уровень пройден!"

        print(f"Player coordinates: x={player.x}, y={player.y}, level_completed={level_completed}")
        return JsonResponse(response_data)

    
    
    def move_player(self, player, dx, dy, game_field):
        new_x = player.x + dx
        new_y = player.y + dy

        print(f"Attempting to move player: current=({player.x}, {player.y}), new=({new_x}, {new_y})")
        print(f"Game field dimensions: width={game_field.width}, height={game_field.height}")

        if not (0 <= new_x < game_field.width*64 and 0 <= new_y < game_field.height*64):
            raise ValueError("Нельзя выйти за пределы игрового поля")
        
        if self.is_cell_occupied(new_x, new_y, game_field):
            raise ValueError("Клетка занята")
        
        player.x = new_x
        player.y = new_y
        player.save()
        print(f"Player moved to: ({player.x}, {player.y})")

        

    def is_cell_occupied(self, x, y, game_field):
        """
        Проверяет, занята ли клетка с координатами (x, y), за исключением объектов с id "goal".
        :param x: Координата X клетки
        :param y: Координата Y клетки
        :param game_field: Объект игрового поля, содержащий список объектов в поле `data`
        :return: True, если клетка занята объектом, на который нельзя перемещаться, иначе False
        """
        for obj in game_field.data:
            if obj["x"] == x and obj["y"] == y:
                if obj["id"] == "goal" or obj["id"] == "player":
                    # Разрешаем перемещение на объект с id "goal"
                    print(f"Cell contains goal: ({x}, {y})")
                    return False
                else:
                    # Блокируем перемещение на все остальные объекты
                    print(f"Cell occupied by object: {obj['id']} at ({x}, {y})")
                    return True
        return False
    
    def post_reset(self, request, pk, user_id):
        print(f"Resetting data for Task ID: {pk}, Player ID: {user_id}")

        # Получаем задачу и игровое поле
        try:
            task = get_object_or_404(Task, pk=pk)
            game_field = get_object_or_404(GameField, id=task.gamefield_id)
        except Exception as e:
            print(f"Error fetching task or game field: {e}")
            return JsonResponse({"error": "Task or game field not found"}, status=404)

        # Пытаемся получить игрока
        try:
            player = Player.objects.get(user_id=user_id, game_field=game_field)
        except Player.DoesNotExist:
            return JsonResponse({"error": "Player not found"}, status=404)

        # Извлекаем данные игрового поля
        try:
            game_field_data = game_field.data  # Предполагается, что это уже список
            if isinstance(game_field_data, str):
                game_field_data = json.loads(game_field_data)  # Преобразуем строку в список
            # Находим объект игрока в данных игрового поля
            player_data = next((item for item in game_field_data if item.get('id') == 'player'), None)
            if player_data:
                # Если нашли игрока, сбрасываем его координаты
                initial_x = player_data.get('x', 0)  # Берем координаты из данных
                initial_y = player_data.get('y', 0)
            else:
                initial_x, initial_y = 0, 0  # Если игрока в данных нет, используем 0, 0
        except Exception as e:
            print(f"Ошибка при обработке данных игрового поля: {e}")
            initial_x, initial_y = 0, 0  # Значения по умолчанию, если не удалось обработать данные

        # Сбрасываем координаты игрока
        player.x = initial_x
        player.y = initial_y
        player.save()
        print(f"Player {user_id} coordinates reset to ({initial_x}, {initial_y})")

        # Сбрасываем код
        try:
            code_entry = Code.objects.get(user_id=user_id, game_field=game_field)
            code_entry.code = ""  # Очищаем код
            code_entry.save()
            print(f"Code for player {user_id} cleared.")
        except Code.DoesNotExist:
            print(f"No code found for player {user_id}. Nothing to clear.")

        return JsonResponse({'status': 'success', 'message': 'Player and code reset successfully'})
        



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

    if record_data == []:
            messages.error(request, "По вашему запросу ничего не найдено")
    
    
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
      
        if journal_data == []:
            messages.error(request, "По вашему запросу ничего не найдено")

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
                request.user.name = name  
                request.user.save()
                messages.success(request, "Имя успешно изменено!")
            else:
                messages.error(request, "Заполните поле имени!")

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
            print(data)
         
            if fields_form.is_valid() and task_form.is_valid():
                game_field = fields_form.save()
                task = task_form.save(commit=False)
                task.gamefield = game_field
                task.save()
                # Извлечение данных playerStart и сохранение в модель Player
                player_data = None
                for obj in data.get('data', []):  # Перебираем массив `data`
                    if obj.get('id') == 'player':  # Ищем объект с id: player
                        player_data = obj
                        break

                if player_data:
                    # Сохраняем положение игрока в модели Player
                    player = Player(
                        game_field=game_field,  # Если Player связан с GameField
                        x=player_data.get('x', 0),
                        y=player_data.get('y', 0)
                    )
                    player.save()
                messages.success(request, "Задача успешно сохранена!")
                return JsonResponse({'status': 'success'})  # Возвращаем JSON-ответ
            else:
                messages.error(request, "Заполните все поля!")

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


    

    