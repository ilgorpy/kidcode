# Generated by Django 5.1.3 on 2024-12-06 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0006_recordview_alter_grade_grade_alter_grade_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='text_exercise',
            field=models.TextField(blank=True, null=True),
        ),
    ]
