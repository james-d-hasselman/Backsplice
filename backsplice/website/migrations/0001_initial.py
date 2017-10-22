# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import website.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.')),
                ('email', models.EmailField(max_length=254, unique=True, error_messages={'unique': 'A user with that username already exists.'}, help_text='Required.', verbose_name='email')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last_name')),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff status', help_text='Designates whether the user can log into the admin site.')),
                ('is_active', models.BooleanField(default=True, verbose_name='active', help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')),
                ('is_approved', models.BooleanField(default=True, verbose_name='approved', help_text='Designates whether this user has been approved for Backsplice access by an administrator.')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(related_query_name='user', verbose_name='groups', to='auth.Group', blank=True, related_name='user_set', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', verbose_name='user permissions', to='auth.Permission', blank=True, related_name='user_set', help_text='Specific permissions for this user.')),
            ],
            options={
                'swappable': 'AUTH_USER_MODEL',
                'verbose_name_plural': 'users',
                'verbose_name': 'user'
            },
        ),
        migrations.AlterModelManagers(
            name='User',
            managers=[
                ('objects', website.models.UserManager()),
            ],
        ),
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
