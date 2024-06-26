# Generated by Django 5.0.4 on 2024-04-26 04:09

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_expense_labels_alter_income_labels'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='expense',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='income',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='expense',
            name='date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='income',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
