# Generated by Django 5.1 on 2024-08-17 10:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserControl', '0003_alter_customusermodel_unique_person_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customusermodel',
            name='unique_person_id',
        ),
    ]
