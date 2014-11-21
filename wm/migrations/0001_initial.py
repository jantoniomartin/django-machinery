# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0001_initial'),
        ('dm', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=128, verbose_name='code')),
                ('description', models.CharField(max_length=255, verbose_name='description')),
                ('measure_unit', models.CharField(max_length=10, null=True, verbose_name='measure unit', blank=True)),
                ('packaging', models.PositiveIntegerField(default=1, verbose_name='standard packaging')),
                ('enabled', models.BooleanField(default=True, verbose_name='enabled')),
                ('control_stock', models.BooleanField(default=False, verbose_name='control stock')),
                ('stock', models.PositiveIntegerField(default=0, verbose_name='stock')),
                ('stock_alert', models.PositiveIntegerField(default=0, verbose_name='stock alert')),
            ],
            options={
                'ordering': ['-id'],
                'verbose_name': 'article',
                'verbose_name_plural': 'articles',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='name')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'brand',
                'verbose_name_plural': 'brands',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name='children', blank=True, to='wm.Group', null=True)),
            ],
            options={
                'verbose_name': 'group',
                'verbose_name_plural': 'groups',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SupplierCode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=50, verbose_name='code')),
                ('article', models.ForeignKey(verbose_name='article', to='wm.Article')),
                ('company', models.ForeignKey(verbose_name='company', to='crm.Company')),
            ],
            options={
                'verbose_name': 'supplier code',
                'verbose_name_plural': 'supplier codes',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='suppliercode',
            unique_together=set([('article', 'company')]),
        ),
        migrations.AddField(
            model_name='article',
            name='brand',
            field=models.ForeignKey(verbose_name='brand', blank=True, to='wm.Brand', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='documents',
            field=models.ManyToManyField(related_name='articles', null=True, verbose_name='documents', to='dm.Document', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='group',
            field=models.ForeignKey(verbose_name='group', to='wm.Group'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='article',
            unique_together=set([('code', 'brand')]),
        ),
    ]
