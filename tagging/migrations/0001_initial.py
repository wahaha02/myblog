
from south.db import db
from django.db import models
from myblog.tagging.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'TaggedItem'
        db.create_table('tagging_taggeditem', (
            ('id', orm['tagging.TaggedItem:id']),
            ('tag', orm['tagging.TaggedItem:tag']),
            ('content_type', orm['tagging.TaggedItem:content_type']),
            ('object_id', orm['tagging.TaggedItem:object_id']),
        ))
        db.send_create_signal('tagging', ['TaggedItem'])
        
        # Adding model 'Tag'
        db.create_table('tagging_tag', (
            ('id', orm['tagging.Tag:id']),
            ('name', orm['tagging.Tag:name']),
        ))
        db.send_create_signal('tagging', ['Tag'])
        
        # Creating unique_together for [tag, content_type, object_id] on TaggedItem.
        db.create_unique('tagging_taggeditem', ['tag_id', 'content_type_id', 'object_id'])
        
    
    
    def backwards(self, orm):
        
        # Deleting unique_together for [tag, content_type, object_id] on TaggedItem.
        db.delete_unique('tagging_taggeditem', ['tag_id', 'content_type_id', 'object_id'])
        
        # Deleting model 'TaggedItem'
        db.delete_table('tagging_taggeditem')
        
        # Deleting model 'Tag'
        db.delete_table('tagging_tag')
        
    
    
    models = {
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'tagging.tag': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'unique': 'True', 'db_index': 'True'})
        },
        'tagging.taggeditem': {
            'Meta': {'unique_together': "(('tag', 'content_type', 'object_id'),)"},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'to': "orm['tagging.Tag']"})
        }
    }
    
    complete_apps = ['tagging']
