# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-23 01:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0006_auto_20171023_0102'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='servicepage',
            options={'ordering': ['-first_published_at'], 'verbose_name': 'Service page', 'verbose_name_plural': 'Services pages'},
        ),
    ]