# -*- coding: utf-8 -*-

from south.db import db
from django.db import models
from myblog.pingback.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'DirectoryPing'
        db.create_table('pingback_directoryping', (
            ('id', orm['pingback.DirectoryPing:id']),
            ('url', orm['pingback.DirectoryPing:url']),
            ('date', orm['pingback.DirectoryPing:date']),
            ('success', orm['pingback.DirectoryPing:success']),
            ('content_type', orm['pingback.DirectoryPing:content_type']),
            ('object_id', orm['pingback.DirectoryPing:object_id']),
        ))
        db.send_create_signal('pingback', ['DirectoryPing'])
        
        # Adding model 'Pingback'
        db.create_table('pingback', (
            ('id', orm['pingback.Pingback:id']),
            ('url', orm['pingback.Pingback:url']),
            ('date', orm['pingback.Pingback:date']),
            ('approved', orm['pingback.Pingback:approved']),
            ('title', orm['pingback.Pingback:title']),
            ('content', orm['pingback.Pingback:content']),
            ('content_type', orm['pingback.Pingback:content_type']),
            ('object_id', orm['pingback.Pingback:object_id']),
        ))
        db.send_create_signal('pingback', ['Pingback'])
        
        # Adding model 'PingbackClient'
        db.create_table('pingback_client', (
            ('id', orm['pingback.PingbackClient:id']),
            ('url', orm['pingback.PingbackClient:url']),
            ('date', orm['pingback.PingbackClient:date']),
            ('success', orm['pingback.PingbackClient:success']),
            ('content_type', orm['pingback.PingbackClient:content_type']),
            ('object_id', orm['pingback.PingbackClient:object_id']),
        ))
        db.send_create_signal('pingback', ['PingbackClient'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'DirectoryPing'
        db.delete_table('pingback_directoryping')
        
        # Deleting model 'Pingback'
        db.delete_table('pingback')
        
        # Deleting model 'PingbackClient'
        db.delete_table('pingback_client')
        
    
    
    models = {
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'pingback.directoryping': {
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'success': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'pingback.pingback': {
            'Meta': {'db_table': "'pingback'"},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'pingback.pingbackclient': {
            'Meta': {'db_table': "'pingback_client'"},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'success': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }
    
    complete_apps = ['pingback']
