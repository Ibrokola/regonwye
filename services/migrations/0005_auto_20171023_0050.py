# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-23 00:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0004_auto_20171023_0043'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='servicepage',
            options={'ordering': ['date'], 'verbose_name': 'Service page', 'verbose_name_plural': 'Services pages'},
        ),
    ]
