# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', uuidfield.fields.UUIDField(unique=True, max_length=32, editable=False, blank=True)),
                ('document', models.FileField(upload_to=b'dm', verbose_name='document')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.CharField(max_length=255, null=True, verbose_name='description', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
            ],
            options={
                'ordering': ['title'],
                'verbose_name': 'document',
                'verbose_name_plural': 'documents',
            },
            bases=(models.Model,),
        ),
    ]
