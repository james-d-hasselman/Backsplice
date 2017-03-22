# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=70)),
                ('week', models.IntegerField()),
                ('period', models.CharField(max_length=15)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='CourseRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('course', models.ForeignKey(to='website.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('first_name', models.CharField(max_length=35)),
                ('last_name', models.CharField(max_length=35)),
                ('middle_name', models.CharField(max_length=35)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Requirement',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('letter', models.CharField(max_length=1)),
                ('text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Scout',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('first_name', models.CharField(max_length=35)),
                ('last_name', models.CharField(max_length=35)),
                ('middle_name', models.CharField(max_length=35)),
                ('unit', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='courserecord',
            name='requirement',
            field=models.ForeignKey(to='website.Requirement'),
        ),
        migrations.AddField(
            model_name='courserecord',
            name='scout',
            field=models.ForeignKey(to='website.Scout'),
        ),
        migrations.AddField(
            model_name='course',
            name='instructor',
            field=models.ForeignKey(to='website.Instructor'),
        ),
        migrations.AddField(
            model_name='course',
            name='requirements',
            field=models.ManyToManyField(to='website.Requirement'),
        ),
    ]
