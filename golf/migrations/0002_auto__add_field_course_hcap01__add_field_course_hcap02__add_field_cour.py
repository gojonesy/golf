# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Course.hcap01'
        db.add_column(u'golf_course', 'hcap01',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Course.hcap02'
        db.add_column(u'golf_course', 'hcap02',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Course.hcap03'
        db.add_column(u'golf_course', 'hcap03',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Course.hcap04'
        db.add_column(u'golf_course', 'hcap04',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Course.hcap05'
        db.add_column(u'golf_course', 'hcap05',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Course.hcap06'
        db.add_column(u'golf_course', 'hcap06',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Course.hcap07'
        db.add_column(u'golf_course', 'hcap07',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Course.hcap08'
        db.add_column(u'golf_course', 'hcap08',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Course.hcap09'
        db.add_column(u'golf_course', 'hcap09',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Course.hcap01'
        db.delete_column(u'golf_course', 'hcap01')

        # Deleting field 'Course.hcap02'
        db.delete_column(u'golf_course', 'hcap02')

        # Deleting field 'Course.hcap03'
        db.delete_column(u'golf_course', 'hcap03')

        # Deleting field 'Course.hcap04'
        db.delete_column(u'golf_course', 'hcap04')

        # Deleting field 'Course.hcap05'
        db.delete_column(u'golf_course', 'hcap05')

        # Deleting field 'Course.hcap06'
        db.delete_column(u'golf_course', 'hcap06')

        # Deleting field 'Course.hcap07'
        db.delete_column(u'golf_course', 'hcap07')

        # Deleting field 'Course.hcap08'
        db.delete_column(u'golf_course', 'hcap08')

        # Deleting field 'Course.hcap09'
        db.delete_column(u'golf_course', 'hcap09')


    models = {
        u'golf.course': {
            'Meta': {'object_name': 'Course'},
            'hcap01': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'hcap02': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'hcap03': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'hcap04': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'hcap05': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'hcap06': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'hcap07': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'hcap08': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'hcap09': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'hole1par': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'hole2par': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'hole3par': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'hole4par': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'hole5par': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'hole6par': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'hole7par': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'hole8par': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'hole9par': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mod_date': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'rating': ('django.db.models.fields.FloatField', [], {}),
            'slope': ('django.db.models.fields.FloatField', [], {})
        },
        u'golf.golfer': {
            'Meta': {'object_name': 'Golfer'},
            'def_handicap': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'email': ('django.db.models.fields.CharField', [], {'default': "'test'", 'max_length': '128', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mod_date': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'phone_alt': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'})
        },
        u'golf.round': {
            'Meta': {'unique_together': "(('week_num', 'year', 'golfer_id'),)", 'object_name': 'Round'},
            'course_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['golf.Course']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'golfer_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['golf.Golfer']"}),
            'hole_1': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'hole_2': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'hole_3': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'hole_4': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'hole_5': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'hole_6': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'hole_7': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'hole_8': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'hole_9': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mod_date': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'week_num': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'year': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'})
        }
    }

    complete_apps = ['golf']