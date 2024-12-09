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


class UserNameChangeForm(forms.Form):
    name = forms.CharField(label="Имя", widget = forms.TextInput(attrs={'class': 'form-input'}), required=False)

class UserPasswordChangeForm(SetPasswordForm):
    new_password1 = forms.CharField(label="Новый пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class FieldsSettingsForm(forms.ModelForm):
    width = forms.IntegerField(label="Ширина", widget = forms.NumberInput(attrs={'class': 'form-input'}))
    height = forms.IntegerField(label="Высота", widget = forms.NumberInput(attrs={'class': 'form-input'}))
    cubes = forms.IntegerField(label="Количество кубиков", widget = forms.NumberInput(attrs={'class': 'form-input'}))
    holes = forms.IntegerField(label="Количество лунок", widget = forms.NumberInput(attrs={'class': 'form-input'}))
    blocks = forms.IntegerField(label="Количество занятых клеток", widget = forms.NumberInput(attrs={'class': 'form-input'}))
    class Meta:
        model = Task
        fields = ['difficult', 'chapter', 'level', 'text_exercise', 'clue', 'deadline']
        labels = {
            'difficult': 'Сложность',
            'chapter': "Глава",
            'level': "Уровень",
            'text_exercise': "Текст упражнения",
            'clue': "Подсказка",
            'deadline': "Дедлайн",
        }
        widgets = {
            'difficult': forms.Select,
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'chapter': forms.TextInput(attrs={'class': 'form-input'}),
            'level': forms.TextInput(attrs={'class': 'form-input'}),
            'text_exercise': forms.Textarea(attrs={'class': 'form-input'}),
            'clue': forms.Textarea(attrs={'class': 'form-input'}),
            'deadline': forms.DateInput(attrs={'class': 'form-input'}),
        }
        choices = Task.difficult
    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            GameField.objects.create(Task = instance, width= self.cleaned_data['width'], height=self.cleaned_data['height'], cubes=self.cleaned_data['cubes'], holes=self.cleaned_data['holes'], blocks=self.cleaned_data['blocks'])
        return instance
    

    