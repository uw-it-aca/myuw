# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-07-26 04:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myuw', '0014_intl_stud_links'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuwnotice',
            name='is_intl_stud',
            field=models.BooleanField(default=False),
        ),
    ]
