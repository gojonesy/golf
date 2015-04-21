# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('golf', '0003_golfer_isactive'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='round',
            unique_together=set([('week_num', 'date', 'golfer_id')]),
        ),
    ]
