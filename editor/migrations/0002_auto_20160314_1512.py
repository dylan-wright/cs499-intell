# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-14 15:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('editor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Scenario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('turn_num', models.IntegerField()),
                ('point_num', models.IntegerField()),
                ('author', models.CharField(max_length=64)),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='scenario',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='editor.Scenario'),
        ),
    ]
