# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-24 03:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20170723_2343'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShelfItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, unique=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('num_items', models.PositiveIntegerField()),
                ('image_url', models.CharField(max_length=350)),
                ('barcode_num', models.IntegerField()),
                ('item_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.ItemType')),
            ],
        ),
        migrations.AddField(
            model_name='supplier',
            name='other_names',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='shelfitem',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Supplier'),
        ),
    ]
