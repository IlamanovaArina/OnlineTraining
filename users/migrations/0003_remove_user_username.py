# Generated by Django 5.1.7 on 2025-03-17 13:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_payments'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
    ]
