# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotation',
            name='created',
            field=models.DateField(verbose_name='created'),
            preserve_default=True,
        ),
    ]
