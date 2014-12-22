# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('wm', '0004_auto_20141127_1531'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['code'], 'verbose_name': 'article', 'verbose_name_plural': 'articles'},
        ),
        migrations.AddField(
            model_name='article',
            name='stock_value',
            field=models.FloatField(default=0, verbose_name='stock value'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='stock_value_updated',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 22, 11, 4, 23, 411594, tzinfo=utc), verbose_name='stock value updated at', editable=False),
            preserve_default=True,
        ),
    ]
