# Generated by Django 4.2.8 on 2023-12-16 13:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tech', '0007_remove_workassignment_comments'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='ispolnitel',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='role',
            field=models.CharField(choices=[('user', 'Пользователь'), ('ispolnitel', 'Исполнитель'), ('admin', 'Администратор')], default='user', max_length=20),
        ),
        migrations.AlterField(
            model_name='request',
            name='client',
            field=models.ForeignKey(limit_choices_to={'role': 'user'}, on_delete=django.db.models.deletion.CASCADE, to='tech.userprofile'),
        ),
        migrations.AlterField(
            model_name='workassignment',
            name='assigned_to',
            field=models.ForeignKey(limit_choices_to={'role': 'ispolnitel'}, on_delete=django.db.models.deletion.CASCADE, to='tech.userprofile'),
        ),
    ]
