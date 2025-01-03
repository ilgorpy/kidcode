from django import forms
from django.contrib.auth import get_user_model
from mainapp.models import GameField, Grade, Code, Task
from django.contrib.auth.forms import SetPasswordForm


class JournalForm(forms.Form):
    status = forms.ChoiceField(choices=Grade.STATUS_CHOICES, label="Статус", widget=forms.Select, required=False)
    level = forms.CharField(label="Уровень", widget = forms.TextInput(attrs={'class': 'form-input'}), required=False)
    name = forms.CharField(label="Имя", widget = forms.TextInput(attrs={'class': 'form-input'}), required=False)

class RecordForm(forms.Form):
    grade = forms.ChoiceField(choices=Grade.GRADES, label="Оценка", widget=forms.Select, required=False)
    level = forms.CharField(label="Уровень", widget = forms.TextInput(attrs={'class': 'form-input'}), required=False)


from django import forms

class UserProfileChangeForm(forms.Form):
    name = forms.CharField(label="Имя", widget=forms.TextInput(attrs={'class': 'form-input'}), required=False)
    new_password1 = forms.CharField(label="Новый пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}), required=False)
    new_password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput(attrs={'class': 'form-input'}), required=False)

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")

        if new_password1 or new_password2:  # Если хотя бы одно поле для пароля заполнено
            if new_password1 != new_password2:
                self.add_error('new_password2', "Пароли не совпадают.")



class FieldsSettingsForm(forms.ModelForm):
    width = forms.IntegerField(label="Ширина", widget=forms.NumberInput(attrs={'class': 'form-input'}), required=True)
    height = forms.IntegerField(label="Высота", widget=forms.NumberInput(attrs={'class': 'form-input'}), required=True)
    cube = forms.IntegerField(label="Количество кубиков", widget=forms.NumberInput(attrs={'class': 'form-input'}), required=True)
    hole = forms.IntegerField(label="Количество лунок", widget=forms.NumberInput(attrs={'class': 'form-input'}), required=True)
    block = forms.IntegerField(label="Количество занятых клеток", widget=forms.NumberInput(attrs={'class': 'form-input'}), required=True)
    
    class Meta:
        model = GameField
        fields = ['width', 'height', 'cube', 'hole', 'block']

class FieldSaveForm(forms.ModelForm):
    class Meta:
        model = GameField
        fields = ['width', 'height', 'cube', 'hole', 'block', 'data']
    
    
    
class TaskTextForm(forms.ModelForm):
      class Meta:
        model = Task
        fields = ['id', 'difficult', 'chapter', 'level', 'text_exercise', 'clue', 'deadline']
        labels = {
            'difficult': 'Сложность',
            'chapter': "Глава",
            'level': "Уровень",
            'text_exercise': "Текст задания",
            'clue': "Подсказка",
            'deadline': "Дедлайн",
        }
        widgets = {
            'difficult': forms.Select(attrs={'class': 'form-input'}),
            'chapter': forms.TextInput(attrs={'class': 'form-input'}),  
            'level': forms.TextInput(attrs={'class': 'form-input'}),
            'text_exercise': forms.Textarea(attrs={'class': 'form-input'}),
            'clue': forms.Textarea(attrs={'class': 'form-input'}),
            'deadline': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
        }
    