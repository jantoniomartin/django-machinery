# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('om', '0002_auto_20141121_1017'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='private_note',
            field=models.CharField(max_length=255, null=True, verbose_name='private note', blank=True),
            preserve_default=True,
        ),
    ]
