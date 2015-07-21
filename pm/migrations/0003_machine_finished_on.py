# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pm', '0002_intervention'),
    ]

    operations = [
        migrations.AddField(
            model_name='machine',
            name='finished_on',
            field=models.DateField(null=True, verbose_name='finished on', blank=True),
            preserve_default=True,
        ),
    ]
