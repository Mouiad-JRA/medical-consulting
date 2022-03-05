# Generated by Django 4.0.2 on 2022-03-05 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_consultation_reply'),
    ]

    operations = [
        migrations.AddField(
            model_name='consultation',
            name='status',
            field=models.CharField(choices=[('answered', 'Answered'), ('hold', 'On Hold')], default='hold', max_length=50, verbose_name='Status'),
        ),
    ]
