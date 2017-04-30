# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_auto_20170410_0244'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursereference',
            name='year',
            field=models.CharField(default='', max_length=4),
            preserve_default=False,
        ),
    ]
