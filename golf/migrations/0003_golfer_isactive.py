# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('golf', '0002_remove_golfer_isactive'),
    ]

    operations = [
        migrations.AddField(
            model_name='golfer',
            name='isActive',
            field=models.BooleanField(default=True),
        ),
    ]
