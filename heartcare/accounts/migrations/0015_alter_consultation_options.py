# Generated by Django 4.0.2 on 2022-03-12 17:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_auto_20220311_1837'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='consultation',
            options={'verbose_name': 'Consultation', 'verbose_name_plural': 'Consultations'},
        ),
    ]