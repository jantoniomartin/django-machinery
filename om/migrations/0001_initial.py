# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.FloatField(verbose_name='quantity')),
            ],
            options={
                'verbose_name': 'cart item',
                'verbose_name_plural': 'cart items',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CsvTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('template', models.CharField(max_length=255, verbose_name='template')),
            ],
            options={
                'verbose_name': 'csv template',
                'verbose_name_plural': 'csv templates',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateField(auto_now_add=True, verbose_name='created on')),
                ('expired_on', models.DateField(null=True, verbose_name='expired on', blank=True)),
                ('code', models.CharField(max_length=50, null=True, verbose_name='offer code', blank=True)),
                ('retail_price', models.FloatField(null=True, verbose_name='retail price', blank=True)),
                ('invoice_price', models.FloatField(null=True, verbose_name='invoice price', blank=True)),
            ],
            options={
                'ordering': ['company', '-created_on'],
                'verbose_name': 'offer',
                'verbose_name_plural': 'offers',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('completed_on', models.DateField(null=True, verbose_name='completed on', blank=True)),
                ('notes', models.CharField(max_length=255, null=True, verbose_name='notes', blank=True)),
                ('company', models.ForeignKey(verbose_name='company', to='crm.Company')),
                ('created_by', models.ForeignKey(verbose_name='created by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-id'],
                'verbose_name': 'order',
                'verbose_name_plural': 'orders',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ordered_quantity', models.FloatField(verbose_name='ordered quantity')),
                ('received_quantity', models.FloatField(default=0, verbose_name='received quantity')),
                ('completed_on', models.DateField(null=True, verbose_name='completed on', blank=True)),
                ('estimated_delivery', models.DateField(null=True, verbose_name='estimated delivery', blank=True)),
                ('offer', models.ForeignKey(verbose_name='offer', to='om.Offer')),
                ('order', models.ForeignKey(verbose_name='order', to='om.Order')),
            ],
            options={
                'ordering': ['-id'],
                'verbose_name': 'order line',
                'verbose_name_plural': 'order lines',
            },
            bases=(models.Model,),
        ),
    ]
