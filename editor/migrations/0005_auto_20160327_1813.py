# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-27 18:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editor', '0004_auto_20160324_1605'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='key',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='description',
            name='key',
            field=models.NullBooleanField(),
        ),
    ]