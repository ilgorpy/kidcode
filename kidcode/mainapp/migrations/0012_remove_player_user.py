# Generated by Django 5.1.3 on 2024-12-23 17:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0011_player'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='user',
        ),
    ]
