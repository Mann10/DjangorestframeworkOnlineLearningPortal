# Generated by Django 5.1 on 2024-08-17 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserControl', '0004_remove_customusermodel_unique_person_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='customusermodel',
            name='unique_person_id',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
