# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_coursereference_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursereference',
            name='instructor',
            field=models.ForeignKey(null=True, to='website.Instructor'),
        ),
    ]
