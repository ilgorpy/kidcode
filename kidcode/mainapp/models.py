from django.db import models

class Task(models.Model):
    name = models.CharField(max_length=100)
    deadline = models.DateField()
    level = models.IntegerField()
    chapter = models.IntegerField()
    clue = models.TextField()


class Grade(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    submission_date = models.DateField(null=True, blank=True)
    grade = models.CharField(max_length=4, choices=[('pass', 'Зачет'), ('fail', 'Не зачет')], null=True, blank=True)
