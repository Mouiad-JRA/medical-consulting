# Generated by Django 4.0.2 on 2022-03-12 18:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_user_is_admin_user_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_admin',
        ),
    ]
