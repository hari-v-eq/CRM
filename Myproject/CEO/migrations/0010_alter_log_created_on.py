# Generated by Django 4.1.1 on 2022-09-27 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CEO', '0009_log'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='created_on',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
