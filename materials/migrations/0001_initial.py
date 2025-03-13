# Generated by Django 5.1.7 on 2025-03-13 17:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название')),
                ('preview', models.ImageField(blank=True, null=True, upload_to='training/', verbose_name='Превью')),
                ('description', models.TextField(max_length=200, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Курс',
                'verbose_name_plural': 'Курсы',
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название')),
                ('preview', models.ImageField(blank=True, null=True, upload_to='training/', verbose_name='Превью')),
                ('description', models.TextField(max_length=200, verbose_name='Описание')),
                ('link_to_video', models.CharField(max_length=100, verbose_name='Ссылка на видео')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='materials.course', verbose_name='Связь с курсом')),
            ],
            options={
                'verbose_name': 'Урок',
                'verbose_name_plural': 'Уроки',
            },
        ),
    ]
