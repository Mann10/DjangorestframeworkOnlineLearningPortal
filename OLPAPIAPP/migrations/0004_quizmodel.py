# Generated by Django 5.1 on 2024-08-20 15:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OLPAPIAPP', '0003_progressmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuizModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Enter the name of the quiz.')),
                ('description', models.TextField(verbose_name='Enter the description for your quiz.')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OLPAPIAPP.coursemodel')),
            ],
        ),
    ]
