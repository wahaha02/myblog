
from south.db import db
from django.db import models
from myblog.blog.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Media'
        db.create_table('blog_media', (
            ('id', orm['blog.Media:id']),
            ('title', orm['blog.Media:title']),
            ('image', orm['blog.Media:image']),
            ('watermarked', orm['blog.Media:watermarked']),
            ('date', orm['blog.Media:date']),
        ))
        db.send_create_signal('blog', ['Media'])
        
        # Adding model 'Post'
        db.create_table('blog_post', (
            ('id', orm['blog.Post:id']),
            ('title', orm['blog.Post:title']),
            ('slug', orm['blog.Post:slug']),
            ('content', orm['blog.Post:content']),
            ('date', orm['blog.Post:date']),
            ('author', orm['blog.Post:author']),
            ('type', orm['blog.Post:type']),
            ('status', orm['blog.Post:status']),
            ('comment_status', orm['blog.Post:comment_status']),
            ('tag', orm['blog.Post:tag']),
        ))
        db.send_create_signal('blog', ['Post'])
        
        # Adding model 'PostMeta'
        db.create_table('blog_postmeta', (
            ('id', orm['blog.PostMeta:id']),
            ('post', orm['blog.PostMeta:post']),
            ('meta_key', orm['blog.PostMeta:meta_key']),
            ('meta_value', orm['blog.PostMeta:meta_value']),
        ))
        db.send_create_signal('blog', ['PostMeta'])
        
        # Adding model 'Link'
        db.create_table('blog_link', (
            ('id', orm['blog.Link:id']),
            ('url', orm['blog.Link:url']),
            ('name', orm['blog.Link:name']),
            ('description', orm['blog.Link:description']),
            ('is_public', orm['blog.Link:is_public']),
        ))
        db.send_create_signal('blog', ['Link'])
        
        # Adding model 'Profile'
        db.create_table('blog_profile', (
            ('id', orm['blog.Profile:id']),
            ('user', orm['blog.Profile:user']),
            ('nickname', orm['blog.Profile:nickname']),
            ('website', orm['blog.Profile:website']),
        ))
        db.send_create_signal('blog', ['Profile'])
        
        # Adding model 'Category'
        db.create_table('blog_category', (
            ('id', orm['blog.Category:id']),
            ('title', orm['blog.Category:title']),
            ('slug', orm['blog.Category:slug']),
            ('description', orm['blog.Category:description']),
        ))
        db.send_create_signal('blog', ['Category'])
        
        # Adding ManyToManyField 'Post.category'
        db.create_table('blog_post_category', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('post', models.ForeignKey(orm.Post, null=False)),
            ('category', models.ForeignKey(orm.Category, null=False))
        ))
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Media'
        db.delete_table('blog_media')
        
        # Deleting model 'Post'
        db.delete_table('blog_post')
        
        # Deleting model 'PostMeta'
        db.delete_table('blog_postmeta')
        
        # Deleting model 'Link'
        db.delete_table('blog_link')
        
        # Deleting model 'Profile'
        db.delete_table('blog_profile')
        
        # Deleting model 'Category'
        db.delete_table('blog_category')
        
        # Dropping ManyToManyField 'Post.category'
        db.delete_table('blog_post_category')
        
    
    
    models = {
        'auth.group': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'blog.category': {
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'unique': 'True', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        'blog.link': {
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'blog.media': {
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'watermarked': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'})
        },
        'blog.post': {
            'author': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'to': "orm['auth.User']"}),
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['blog.Category']"}),
            'comment_status': ('django.db.models.fields.CharField', [], {'default': "'open'", 'max_length': '20'}),
            'comments': ('django.contrib.contenttypes.generic.GenericRelation', [], {'object_id_field': "'object_pk'", 'to': "orm['comments.Comment']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '50', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'publish'", 'max_length': '20'}),
            'tag': ('TagField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'post'", 'max_length': '20'})
        },
        'blog.postmeta': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meta_key': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'meta_value': ('django.db.models.fields.TextField', [], {}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['blog.Post']"})
        },
        'blog.profile': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'comments.comment': {
            'content': ('django.db.models.fields.TextField', [], {'max_length': '3000'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'None'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_removed': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'mail_notify': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'object_pk': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'children'", 'blank': 'True', 'null': 'True', 'to': "orm['comments.Comment']"}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comment for comment'", 'to': "orm['sites.Site']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'user_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'user_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'user_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'sites.site': {
            'Meta': {'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }
    
    complete_apps = ['blog']
