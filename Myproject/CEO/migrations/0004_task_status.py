# Generated by Django 4.1.1 on 2022-09-22 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CEO', '0003_remove_task_email_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='status',
            field=models.CharField(default='Pending', max_length=20),
        ),
    ]