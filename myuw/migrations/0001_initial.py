# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CourseColor'
        db.create_table(u'myuw_mobile_coursecolor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('regid', self.gf('django.db.models.fields.CharField')(max_length=32, db_index=True)),
            ('year', self.gf('django.db.models.fields.PositiveSmallIntegerField')(db_index=True)),
            ('quarter', self.gf('django.db.models.fields.CharField')(max_length=10, db_index=True)),
            ('curriculum_abbr', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('course_number', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('section_id', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')()),
            ('color_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'myuw', ['CourseColor'])

        # Adding model 'User'
        db.create_table(u'myuw_mobile_user', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uwnetid', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=16)),
            ('uwregid', self.gf('django.db.models.fields.CharField')(max_length=32, unique=True, null=True, db_index=True)),
            ('last_visit', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 9, 12, 0, 0))),
        ))
        db.send_create_signal(u'myuw', ['User'])

        # Adding model 'Building'
        db.create_table(u'myuw_mobile_building', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=6, db_index=True)),
            ('latititude', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('longitude', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'myuw', ['Building'])

        # Adding model 'StudentAccountsBalances'
        db.create_table(u'myuw_mobile_studentaccountsbalances', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('student_number', self.gf('django.db.models.fields.CharField')(unique=True, max_length=10, db_index=True)),
            ('employee_id', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=10, null=True, blank=True)),
            ('asof_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('is_am', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('husky_card', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=6, decimal_places=2)),
            ('residence_hall_dining', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=7, decimal_places=2, blank=True)),
        ))
        db.send_create_signal(u'myuw', ['StudentAccountsBalances'])

        # Adding model 'UserNotices'
        db.create_table(u'myuw_mobile_usernotices', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('notice_hash', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['myuw_mobile.User'], on_delete=models.PROTECT)),
            ('first_viewed', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('marked_read', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('is_read', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'myuw', ['UserNotices'])

        # Adding model 'CategoryLinks'
        db.create_table(u'myuw_mobile_categorylinks', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('campus', self.gf('django.db.models.fields.CharField')(max_length=8, null=True)),
            ('category_id', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('category_name', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('sub_category', self.gf('django.db.models.fields.CharField')(max_length=80)),
        ))
        db.send_create_signal(u'myuw', ['CategoryLinks'])

        # Adding model 'TuitionDate'
        db.create_table(u'myuw_mobile_tuitiondate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['myuw_mobile.User'], unique=True, on_delete=models.PROTECT)),
            ('date_stored', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'myuw', ['TuitionDate'])


    def backwards(self, orm):
        # Deleting model 'CourseColor'
        db.delete_table(u'myuw_mobile_coursecolor')

        # Deleting model 'User'
        db.delete_table(u'myuw_mobile_user')

        # Deleting model 'Building'
        db.delete_table(u'myuw_mobile_building')

        # Deleting model 'StudentAccountsBalances'
        db.delete_table(u'myuw_mobile_studentaccountsbalances')

        # Deleting model 'UserNotices'
        db.delete_table(u'myuw_mobile_usernotices')

        # Deleting model 'CategoryLinks'
        db.delete_table(u'myuw_mobile_categorylinks')

        # Deleting model 'TuitionDate'
        db.delete_table(u'myuw_mobile_tuitiondate')


    models = {
        u'myuw_mobile.building': {
            'Meta': {'object_name': 'Building'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '6', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latititude': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'longitude': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'myuw_mobile.categorylinks': {
            'Meta': {'object_name': 'CategoryLinks'},
            'campus': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True'}),
            'category_id': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'category_name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sub_category': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        u'myuw_mobile.coursecolor': {
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
        u'myuw_mobile.studentaccountsbalances': {
            'Meta': {'object_name': 'StudentAccountsBalances'},
            'asof_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'employee_id': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'husky_card': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '6', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_am': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'residence_hall_dining': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '2', 'blank': 'True'}),
            'student_number': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10', 'db_index': 'True'})
        },
        u'myuw_mobile.tuitiondate': {
            'Meta': {'object_name': 'TuitionDate'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'date_stored': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['myuw_mobile.User']", 'unique': 'True', 'on_delete': 'models.PROTECT'})
        },
        u'myuw_mobile.user': {
            'Meta': {'object_name': 'User'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_visit': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 12, 0, 0)'}),
            'uwnetid': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '16'}),
            'uwregid': ('django.db.models.fields.CharField', [], {'max_length': '32', 'unique': 'True', 'null': 'True', 'db_index': 'True'})
        },
        u'myuw_mobile.usernotices': {
            'Meta': {'object_name': 'UserNotices'},
            'first_viewed': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_read': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'marked_read': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'notice_hash': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['myuw_mobile.User']", 'on_delete': 'models.PROTECT'})
        }
    }

    complete_apps = ['myuw_mobile']
