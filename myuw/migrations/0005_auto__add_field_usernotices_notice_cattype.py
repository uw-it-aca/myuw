# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'UserNotices.notice_cattype'
        db.add_column('myuw_mobile_usernotices', 'notice_cattype',
                      self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'UserNotices.notice_cattype'
        db.delete_column('myuw_mobile_usernotices', 'notice_cattype')


    models = {
        'myuw.building': {
            'Meta': {'object_name': 'Building', 'db_table': "'myuw_mobile_building'"},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '6', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latititude': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'longitude': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'myuw.categorylinks': {
            'Meta': {'object_name': 'CategoryLinks', 'db_table': "'myuw_mobile_categorylinks'"},
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
            'Meta': {'object_name': 'CourseColor', 'db_table': "'myuw_mobile_coursecolor'"},
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
            'Meta': {'object_name': 'SeenRegistration', 'db_table': "'myuw_mobile_seenregistration'"},
            'first_seen_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'quarter': ('django.db.models.fields.CharField', [], {'max_length': '10', 'db_index': 'True'}),
            'summer_term': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['myuw.User']", 'on_delete': 'models.PROTECT'}),
            'year': ('django.db.models.fields.PositiveSmallIntegerField', [], {'db_index': 'True'})
        },
        u'myuw.studentaccountsbalances': {
            'Meta': {'object_name': 'StudentAccountsBalances', 'db_table': "'myuw_mobile_studentaccountsbalances'"},
            'asof_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'employee_id': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'husky_card': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '6', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_am': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'residence_hall_dining': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '2', 'blank': 'True'}),
            'student_number': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10', 'db_index': 'True'})
        },
        u'myuw.tuitiondate': {
            'Meta': {'object_name': 'TuitionDate', 'db_table': "'myuw_mobile_tuitiondate'"},
            'date': ('django.db.models.fields.DateField', [], {}),
            'date_stored': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['myuw.User']", 'unique': 'True', 'on_delete': 'models.PROTECT'})
        },
        u'myuw.user': {
            'Meta': {'object_name': 'User', 'db_table': "'myuw_mobile_user'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_visit': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 9, 5, 0, 0)'}),
            'uwnetid': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '16'}),
            'uwregid': ('django.db.models.fields.CharField', [], {'max_length': '32', 'unique': 'True', 'null': 'True', 'db_index': 'True'})
        },
        u'myuw.usermigrationpreference': {
            'Meta': {'object_name': 'UserMigrationPreference'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'use_legacy_site': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20', 'db_index': 'True'})
        },
        u'myuw.usernotices': {
            'Meta': {'unique_together': "(('notice_hash', 'user'),)", 'object_name': 'UserNotices', 'db_table': "'myuw_mobile_usernotices'"},
            'first_viewed': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_read': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'marked_read': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'notice_cattype': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'notice_hash': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['myuw.User']", 'on_delete': 'models.PROTECT'})
        }
    }

    complete_apps = ['myuw']