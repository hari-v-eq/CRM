# Generated by Django 4.1.1 on 2022-09-26 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CEO', '0006_alter_task_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('message', models.TextField(max_length=200)),
                ('status', models.CharField(default='Pending', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AlterField(
            model_name='task',
            name='title',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
