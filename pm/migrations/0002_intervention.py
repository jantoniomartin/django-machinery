# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
        ('pm', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Intervention',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_at', models.DateTimeField(verbose_name='start at')),
                ('end_at', models.DateTimeField(null=True, verbose_name='end at', blank=True)),
                ('seconds', models.PositiveIntegerField(default=0, verbose_name='seconds', editable=False)),
                ('employee', models.ForeignKey(verbose_name='employee', to='profiles.Employee')),
                ('machine', models.ForeignKey(verbose_name='machine', to='pm.Machine')),
            ],
            options={
                'verbose_name': 'intervention',
                'verbose_name_plural': 'interventions',
            },
            bases=(models.Model,),
        ),
    ]
