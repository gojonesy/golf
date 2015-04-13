# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128)),
                ('rating', models.FloatField()),
                ('slope', models.FloatField()),
                ('hole1par', models.IntegerField(default=0)),
                ('hole2par', models.IntegerField(default=0)),
                ('hole3par', models.IntegerField(default=0)),
                ('hole4par', models.IntegerField(default=0)),
                ('hole5par', models.IntegerField(default=0)),
                ('hole6par', models.IntegerField(default=0)),
                ('hole7par', models.IntegerField(default=0)),
                ('hole8par', models.IntegerField(default=0)),
                ('hole9par', models.IntegerField(default=0)),
                ('hcap01', models.IntegerField(default=0)),
                ('hcap02', models.IntegerField(default=0)),
                ('hcap03', models.IntegerField(default=0)),
                ('hcap04', models.IntegerField(default=0)),
                ('hcap05', models.IntegerField(default=0)),
                ('hcap06', models.IntegerField(default=0)),
                ('hcap07', models.IntegerField(default=0)),
                ('hcap08', models.IntegerField(default=0)),
                ('hcap09', models.IntegerField(default=0)),
                ('mod_date', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Golfer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('last_name', models.CharField(max_length=128, null=True, blank=True)),
                ('first_name', models.CharField(max_length=128, null=True, blank=True)),
                ('email', models.CharField(default=b'test', max_length=128, null=True, blank=True)),
                ('phone', models.CharField(max_length=128, null=True, blank=True)),
                ('phone_alt', models.CharField(max_length=128, null=True, blank=True)),
                ('def_handicap', models.IntegerField(default=0)),
                ('handicap', models.IntegerField(default=0, null=True, blank=True)),
                ('skins', models.BooleanField(default=False)),
                ('isActive', models.BooleanField(default=True)),
                ('mod_date', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Round',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('year', models.IntegerField(default=0, blank=True)),
                ('week_num', models.IntegerField(default=0)),
                ('hole_1', models.IntegerField(default=0)),
                ('hole_2', models.IntegerField(default=0)),
                ('hole_3', models.IntegerField(default=0)),
                ('hole_4', models.IntegerField(default=0)),
                ('hole_5', models.IntegerField(default=0)),
                ('hole_6', models.IntegerField(default=0)),
                ('hole_7', models.IntegerField(default=0)),
                ('hole_8', models.IntegerField(default=0)),
                ('hole_9', models.IntegerField(default=0)),
                ('points', models.FloatField(default=0.0, null=True, blank=True)),
                ('mod_points', models.FloatField(default=0.0, null=True, blank=True)),
                ('cur_handicap', models.IntegerField(default=0, null=True, blank=True)),
                ('mod_date', models.DateField(auto_now=True)),
                ('course_id', models.ForeignKey(to='golf.Course')),
                ('golfer_id', models.ForeignKey(to='golf.Golfer')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='round',
            unique_together=set([('week_num', 'year', 'golfer_id')]),
        ),
    ]
