# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_auto_20170517_2117'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='requirement',
            name='course_name',
        ),
        migrations.AddField(
            model_name='requirement',
            name='course_reference',
            field=models.ForeignKey(to='website.CourseReference', default=0),
            preserve_default=False,
        ),
    ]
