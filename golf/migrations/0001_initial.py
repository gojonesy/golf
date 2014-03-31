# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Golfer'
        db.create_table(u'golf_golfer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('mod_date', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'golf', ['Golfer'])

        # Adding model 'Course'
        db.create_table(u'golf_course', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
            ('rating', self.gf('django.db.models.fields.FloatField')()),
            ('slope', self.gf('django.db.models.fields.FloatField')()),
            ('hole1par', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('hole2par', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('hole3par', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('hole4par', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('hole5par', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('hole6par', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('hole7par', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('hole8par', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('hole9par', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('mod_date', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'golf', ['Course'])

        # Adding model 'Round'
        db.create_table(u'golf_round', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('golfer_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['golf.Golfer'])),
            ('course_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['golf.Course'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('year', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('week_num', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('hole_1', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('hole_2', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('hole_3', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('hole_4', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('hole_5', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('hole_6', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('hole_7', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('hole_8', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('hole_9', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('mod_date', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'golf', ['Round'])

        # Adding unique constraint on 'Round', fields ['week_num', 'year', 'golfer_id']
        db.create_unique(u'golf_round', ['week_num', 'year', 'golfer_id_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Round', fields ['week_num', 'year', 'golfer_id']
        db.delete_unique(u'golf_round', ['week_num', 'year', 'golfer_id_id'])

        # Deleting model 'Golfer'
        db.delete_table(u'golf_golfer')

        # Deleting model 'Course'
        db.delete_table(u'golf_course')

        # Deleting model 'Round'
        db.delete_table(u'golf_round')


    models = {
        u'golf.course': {
            'Meta': {'object_name': 'Course'},
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
            'email': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mod_date': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '128'})
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