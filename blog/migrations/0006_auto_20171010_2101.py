# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-10 21:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20171010_2053'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='BlofPageGalleryImage',
            new_name='BlogPageGalleryImage',
        ),
    ]