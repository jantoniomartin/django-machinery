# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import pm.models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wm', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CECertificate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(verbose_name='date')),
            ],
            options={
                'verbose_name': 'CE certificate',
                'verbose_name_plural': 'CE certificates',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('model', models.CharField(max_length=3, verbose_name='model')),
                ('number', models.CharField(max_length=2, verbose_name='number')),
                ('description', models.CharField(max_length=255, verbose_name='description')),
                ('created_on', models.DateField(auto_now_add=True, verbose_name='created on', null=True)),
                ('shipped_on', models.DateField(null=True, verbose_name='shipped on', blank=True)),
                ('running_on', models.DateField(null=True, verbose_name='running on', blank=True)),
                ('estimated_delivery_on', models.DateField(null=True, verbose_name='estimated delivery', blank=True)),
                ('is_retired', models.BooleanField(default=False, verbose_name='retired')),
                ('contract_item', models.ForeignKey(verbose_name='contract item', blank=True, to='crm.ContractItem', null=True)),
            ],
            options={
                'ordering': ['number'],
                'verbose_name': 'machine',
                'verbose_name_plural': 'machines',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MachineComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('body', models.TextField(verbose_name='body')),
                ('created_on', models.DateField(auto_now_add=True, verbose_name='created on')),
                ('author', models.ForeignKey(verbose_name='author', to=settings.AUTH_USER_MODEL)),
                ('machine', models.ForeignKey(verbose_name='machine', to='pm.Machine')),
            ],
            options={
                'verbose_name': 'machine comment',
                'verbose_name_plural': 'machine comments',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Part',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.FloatField(verbose_name='quantity')),
                ('function', models.CharField(max_length=255, verbose_name='function')),
                ('article', models.ForeignKey(verbose_name='article', to='wm.Article')),
                ('machine', models.ForeignKey(verbose_name='machine', to='pm.Machine')),
            ],
            options={
                'ordering': ['pk'],
                'verbose_name': 'part',
                'verbose_name_plural': 'parts',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('serial', models.CharField(max_length=4, verbose_name='serial number')),
                ('old_model', models.CharField(max_length=5, null=True, verbose_name='old model', blank=True)),
                ('description', models.CharField(max_length=255, verbose_name='description')),
                ('notes', models.TextField(null=True, verbose_name='notes', blank=True)),
                ('is_retired', models.BooleanField(default=False, verbose_name='retired')),
                ('created_on', models.DateField(auto_now_add=True, verbose_name='created on', null=True)),
                ('thumbnail', models.ImageField(upload_to=pm.models.project_thumbnail, null=True, verbose_name='thumbnail', blank=True)),
                ('company', models.ForeignKey(verbose_name='company', to='crm.Company')),
            ],
            options={
                'ordering': ['-serial'],
                'verbose_name': 'project',
                'verbose_name_plural': 'projects',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=3, verbose_name='code')),
                ('description', models.CharField(max_length=50, verbose_name='description')),
            ],
            options={
                'verbose_name': 'sector',
                'verbose_name_plural': 'sectors',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='created on')),
                ('updated_on', models.DateTimeField(auto_now=True, verbose_name='updated on')),
                ('status', models.PositiveIntegerField(default=0, verbose_name='status', choices=[(0, 'The customer is waiting for an answer'), (1, 'Waiting for an answer from the customer'), (2, 'Closed')])),
                ('summary', models.CharField(max_length=255, verbose_name='summary')),
                ('content', models.TextField(verbose_name='content')),
                ('project', models.ForeignKey(verbose_name='project', to='pm.Project')),
                ('updated_by', models.ForeignKey(verbose_name='updated by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-updated_on'],
                'verbose_name': 'ticket',
                'verbose_name_plural': 'tickets',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TicketItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='created on')),
                ('content', models.TextField(verbose_name='content')),
                ('created_by', models.ForeignKey(verbose_name='created_by', to=settings.AUTH_USER_MODEL)),
                ('ticket', models.ForeignKey(verbose_name='ticket', to='pm.Ticket')),
            ],
            options={
                'verbose_name': 'ticket item',
                'verbose_name_plural': 'ticket items',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='project',
            name='sector',
            field=models.ForeignKey(verbose_name='sector', to='pm.Sector'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='machine',
            name='project',
            field=models.ForeignKey(verbose_name='project', to='pm.Project'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='machine',
            unique_together=set([('number', 'project')]),
        ),
        migrations.AddField(
            model_name='cecertificate',
            name='project',
            field=models.ForeignKey(verbose_name='project', to='pm.Project'),
            preserve_default=True,
        ),
    ]
