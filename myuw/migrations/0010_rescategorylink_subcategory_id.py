# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-29 22:46
from __future__ import unicode_literals
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myuw', '0009_resourcecategorypin'),
    ]

    operations = [
        migrations.AddField(
            model_name='rescategorylink',
            name='subcategory_id',
            field=models.CharField(max_length=80, null=True),
        ),
    ]
