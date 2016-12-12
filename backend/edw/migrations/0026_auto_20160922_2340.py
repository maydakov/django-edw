# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-09-22 20:40
from __future__ import unicode_literals

from django.db import migrations
import django.db.models.deletion
import filer.fields.file


class Migration(migrations.Migration):

    dependencies = [
        ('edw', '0025_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificationattachment',
            name='attachment',
            field=filer.fields.file.FilerFileField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='email_attachment', to='filer.File', verbose_name='Attachment'),
        ),
    ]