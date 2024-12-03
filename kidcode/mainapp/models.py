from django.db import models

class Task(models.Model):
    name = models.CharField(max_length=100)
    deadline = models.DateField()
    level = models.IntegerField()
    chapter = models.IntegerField()
    clue = models.TextField()
    difficult = models.CharField(max_length=6, choices=[('easy', 'Легкий'), ('medium', 'Средний'), ('hard', 'Сложный')])
    gamefield = models.ForeignKey('GameField', on_delete=models.CASCADE)


class Grade(models.Model):
    STATUS_CHOICES = [
    ('sended', 'Отправлено'),
    ('not_sended', 'Не отправлено'),
    ]
    GRADES = [
        ('pass', 'зачет'),
        ('fail', 'не зачет'),
    ]
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, null=True, blank=True)
    grade = models.CharField(max_length=4, choices=GRADES, null=True, blank=True)
    submission_date = models.DateField(null=True, blank=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    code = models.ForeignKey('Code', on_delete=models.CASCADE)


class Code(models.Model):
    code = models.TextField()


class GameField(models.Model):
    width = models.IntegerField()
    height = models.IntegerField()
    cube = models.IntegerField()
    hole = models.IntegerField()
    block = models.IntegerField()
