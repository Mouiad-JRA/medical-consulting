# Generated by Django 3.2 on 2022-03-05 19:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0003_service_created_date_service_updated_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='service',
            options={'verbose_name': 'medical topics', 'verbose_name_plural': 'medical topics'},
        ),
    ]
