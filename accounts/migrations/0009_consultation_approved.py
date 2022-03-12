# Generated by Django 3.2 on 2022-03-05 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_user_approved'),
    ]

    operations = [
        migrations.AddField(
            model_name='consultation',
            name='approved',
            field=models.BooleanField(blank=True, default=False, verbose_name='Is Approved'),
        ),
    ]