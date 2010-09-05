
from south.db import db
from django.db import models
from myblog.rabidratings.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Rating'
        db.create_table('rabidratings_rating', (
            ('id', orm['rabidratings.Rating:id']),
            ('key', orm['rabidratings.Rating:key']),
            ('total_rating', orm['rabidratings.Rating:total_rating']),
            ('total_votes', orm['rabidratings.Rating:total_votes']),
            ('avg_rating', orm['rabidratings.Rating:avg_rating']),
            ('percent', orm['rabidratings.Rating:percent']),
        ))
        db.send_create_signal('rabidratings', ['Rating'])
        
        # Adding model 'RatingEvent'
        db.create_table('rabidratings_ratingevent', (
            ('id', orm['rabidratings.RatingEvent:id']),
            ('key', orm['rabidratings.RatingEvent:key']),
            ('ip', orm['rabidratings.RatingEvent:ip']),
            ('date', orm['rabidratings.RatingEvent:date']),
            ('value', orm['rabidratings.RatingEvent:value']),
        ))
        db.send_create_signal('rabidratings', ['RatingEvent'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Rating'
        db.delete_table('rabidratings_rating')
        
        # Deleting model 'RatingEvent'
        db.delete_table('rabidratings_ratingevent')
        
    
    
    models = {
        'rabidratings.rating': {
            'avg_rating': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True'}),
            'percent': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'total_rating': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'total_votes': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'rabidratings.ratingevent': {
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'value': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }
    
    complete_apps = ['rabidratings']
