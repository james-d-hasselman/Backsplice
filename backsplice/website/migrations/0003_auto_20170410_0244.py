# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_course_scouts'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseReference',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=70)),
                ('period', models.CharField(max_length=15)),
                ('instructor', models.ForeignKey(to='website.Instructor')),
            ],
        ),
        migrations.RemoveField(
            model_name='course',
            name='instructor',
        ),
        migrations.RemoveField(
            model_name='course',
            name='name',
        ),
        migrations.RemoveField(
            model_name='course',
            name='period',
        ),
        migrations.RemoveField(
            model_name='course',
            name='requirements',
        ),
        migrations.AddField(
            model_name='requirement',
            name='course_name',
            field=models.CharField(max_length=70, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='course',
            name='course_reference',
            field=models.ForeignKey(to='website.CourseReference', default=1),
            preserve_default=False,
        ),
    ]
