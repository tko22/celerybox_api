# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-24 22:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_auto_20170724_0632'),
    ]

    operations = [
        migrations.CreateModel(
            name='SupplierAlias',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alias', models.CharField(max_length=5)),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Supplier')),
            ],
        ),
    ]
