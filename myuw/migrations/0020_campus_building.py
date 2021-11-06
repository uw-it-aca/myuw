# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myuw', '0019_seenregistration'),
    ]

    operations = [
        migrations.CreateModel(
            name='Buildings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(db_index=True, max_length=10)),
                ('number', models.CharField(db_index=True, max_length=10)),
                ('latititude', models.CharField(max_length=40)),
                ('longitude', models.CharField(max_length=40)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'myuw_campus_buildings',
            },
        ),
    ]
