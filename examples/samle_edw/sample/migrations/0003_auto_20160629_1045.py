# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-29 07:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sample', '0002_auto_20160628_2241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booktranslation',
            name='description',
            field=models.TextField(blank=True, help_text='Description for the list view of books.', null=True, verbose_name='Description'),
        ),
    ]
