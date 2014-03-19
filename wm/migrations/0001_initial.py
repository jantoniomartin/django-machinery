# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Brand'
        db.create_table(u'wm_brand', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'wm', ['Brand'])

        # Adding model 'Group'
        db.create_table(u'wm_group', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, to=orm['wm.Group'])),
            (u'lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal(u'wm', ['Group'])

        # Adding model 'Article'
        db.create_table(u'wm_article', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('measure_unit', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('packaging', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('brand', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wm.Brand'], null=True, blank=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wm.Group'])),
            ('control_stock', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('stock', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('stock_alert', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal(u'wm', ['Article'])

        # Adding unique constraint on 'Article', fields ['code', 'brand']
        db.create_unique(u'wm_article', ['code', 'brand_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Article', fields ['code', 'brand']
        db.delete_unique(u'wm_article', ['code', 'brand_id'])

        # Deleting model 'Brand'
        db.delete_table(u'wm_brand')

        # Deleting model 'Group'
        db.delete_table(u'wm_group')

        # Deleting model 'Article'
        db.delete_table(u'wm_article')


    models = {
        u'wm.article': {
            'Meta': {'ordering': "['-id']", 'unique_together': "[('code', 'brand')]", 'object_name': 'Article'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['wm.Brand']", 'null': 'True', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'control_stock': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['wm.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'measure_unit': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'packaging': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'stock': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'stock_alert': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        u'wm.brand': {
            'Meta': {'ordering': "['name']", 'object_name': 'Brand'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'wm.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['wm.Group']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        }
    }

    complete_apps = ['wm']