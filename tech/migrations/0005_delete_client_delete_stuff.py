# Generated by Django 4.2.8 on 2023-12-11 13:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tech', '0004_userprofile_alter_request_client_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Client',
        ),
        migrations.DeleteModel(
            name='Stuff',
        ),
    ]
