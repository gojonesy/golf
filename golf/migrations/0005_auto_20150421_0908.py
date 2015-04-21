# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('golf', '0004_auto_20150421_0907'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='round',
            unique_together=set([('week_num', 'year', 'golfer_id')]),
        ),
    ]
