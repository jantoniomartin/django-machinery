# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('wm', '0003_article_stock_updated'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='price',
            field=models.FloatField(null=True, verbose_name='retail price', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='price_updated',
            field=models.DateTimeField(default=datetime.datetime(2014, 11, 27, 15, 31, 21, 79037, tzinfo=utc), verbose_name='price updated at'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='article',
            name='stock_updated',
            field=models.DateTimeField(default=datetime.datetime(2014, 11, 27, 15, 31, 21, 78870, tzinfo=utc), verbose_name='stock updated at'),
            preserve_default=True,
        ),
    ]
