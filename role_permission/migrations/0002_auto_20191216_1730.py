# Generated by Django 2.2.7 on 2019-12-16 17:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('role_permission', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='role',
            name='company_id',
        ),
        migrations.RemoveField(
            model_name='rolepermission',
            name='company_id',
        ),
    ]
