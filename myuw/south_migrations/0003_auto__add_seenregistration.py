# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SeenRegistration'
        db.create_table(u'myuw_mobile_seenregistration', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['myuw.User'], on_delete=models.PROTECT)),
            ('year', self.gf('django.db.models.fields.PositiveSmallIntegerField')(db_index=True)),
            ('quarter', self.gf('django.db.models.fields.CharField')(max_length=10, db_index=True)),
            ('summer_term', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('first_seen_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'myuw', ['SeenRegistration'])


    def backwards(self, orm):
        # Deleting model 'SeenRegistration'
        db.delete_table(u'myuw_mobile_seenregistration')


    models = {
        u'myuw.building': {
            'Meta': {'object_name': 'Building'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '6', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latititude': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'longitude': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'myuw.categorylinks': {
            'Meta': {'object_name': 'CategoryLinks'},
            'campus': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True'}),
            'category_id': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'category_name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new_tab': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sub_category': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        u'myuw.coursecolor': {
            'Meta': {'object_name': 'CourseColor'},
            'color_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'course_number': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'curriculum_abbr': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {}),
            'quarter': ('django.db.models.fields.CharField', [], {'max_length': '10', 'db_index': 'True'}),
            'regid': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_index': 'True'}),
            'section_id': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'year': ('django.db.models.fields.PositiveSmallIntegerField', [], {'db_index': 'True'})
        },
        u'myuw.seenregistration': {
            'Meta': {'object_name': 'SeenRegistration'},
            'first_seen_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'quarter': ('django.db.models.fields.CharField', [], {'max_length': '10', 'db_index': 'True'}),
            'summer_term': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['myuw.User']", 'on_delete': 'models.PROTECT'}),
            'year': ('django.db.models.fields.PositiveSmallIntegerField', [], {'db_index': 'True'})
        },
        u'myuw.studentaccountsbalances': {
            'Meta': {'object_name': 'StudentAccountsBalances'},
            'asof_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'employee_id': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'husky_card': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '6', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_am': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'residence_hall_dining': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '2', 'blank': 'True'}),
            'student_number': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10', 'db_index': 'True'})
        },
        u'myuw.tuitiondate': {
            'Meta': {'object_name': 'TuitionDate'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'date_stored': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['myuw.User']", 'unique': 'True', 'on_delete': 'models.PROTECT'})
        },
        u'myuw.user': {
            'Meta': {'object_name': 'User'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_visit': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 10, 27, 0, 0)'}),
            'uwnetid': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '16'}),
            'uwregid': ('django.db.models.fields.CharField', [], {'max_length': '32', 'unique': 'True', 'null': 'True', 'db_index': 'True'})
        },
        u'myuw.usernotices': {
            'Meta': {'unique_together': "(('notice_hash', 'user'),)", 'object_name': 'UserNotices'},
            'first_viewed': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_read': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'marked_read': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'notice_hash': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['myuw.User']", 'on_delete': 'models.PROTECT'})
        }
    }

    complete_apps = ['myuw']
