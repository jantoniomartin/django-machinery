# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pm', '0003_machine_finished_on'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='hide',
            field=models.BooleanField(default=False, verbose_name='hide from dashboard'),
            preserve_default=True,
        ),
    ]
