from django.db import models

def jsonfield_default_value():  # This is a callable
    return [0, 0]

class Task(models.Model):
    deadline = models.DateField()
    level = models.CharField(max_length=100)
    chapter = models.CharField(max_length=100)
    clue = models.TextField()
    text_exercise = models.TextField(blank=True, null=True)
    difficult = models.CharField(max_length=6, choices=[('easy', 'Легкий'), ('medium', 'Средний'), ('hard', 'Сложный')])
    gamefield = models.ForeignKey('GameField', on_delete=models.CASCADE)


class Grade(models.Model):
    STATUS_CHOICES = [
        ('', 'Любой'),
        ('sended', 'Отправлено'),
        ('not_sended', 'Не отправлено'),
    ]
    GRADES = [
        ('', 'Любой'),
        ('pass', 'зачет'),
        ('fail', 'не зачет'),
    ]
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, null=True, blank=True)
    grade = models.CharField(max_length=4, choices=GRADES, null=True, blank=True)
    submission_date = models.DateField(null=True, blank=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    code = models.ForeignKey('Code', on_delete=models.CASCADE)


class Player(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, default=21)
    game_field = models.ForeignKey('GameField', on_delete=models.CASCADE)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)

class Code(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, default=21)
    game_field = models.ForeignKey('GameField', on_delete=models.CASCADE, default=1)
    code = models.TextField()

    class Meta:
        unique_together = ('user', 'game_field') 


class GameField(models.Model):
    width = models.IntegerField()
    height = models.IntegerField()
    cube = models.IntegerField()
    hole = models.IntegerField()
    block = models.IntegerField()
    data = models.JSONField(default= jsonfield_default_value)


class JournalViewManager(models.Manager):
    def get_queryset(self):
        fields = [field.name for field in JournalView._meta.fields]  # Получаем имена полей как строки
        return super().get_queryset().values(*fields)
       

class JournalView(models.Model):
    objects = JournalViewManager()
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=100)
    task_id = models.IntegerField()
    submission_date = models.DateField()
    status = models.CharField(max_length=15)
    grade = models.CharField(max_length=4)
    code = models.TextField()
    grade_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'newview'

class JournalViewManager(models.Manager):
    def get_queryset(self):
        fields = [field.name for field in RecordView._meta.fields]
        return super().get_queryset().values(*fields)
    
class RecordView(models.Model):
    grade = models.CharField(max_length=4)
    level = models.CharField(max_length=100)
    chapter = models.CharField(max_length=100)
    submission_date = models.DateField()
    deadline = models.DateField()
    user_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'newview_1'
    
