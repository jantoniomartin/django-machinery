# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('wm', '0005_auto_20141222_1104'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='favorited',
            field=models.BooleanField(default=False, verbose_name='favorited'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='article',
            name='price_updated',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 9, 10, 3, 5, 421715, tzinfo=utc), verbose_name='price updated at', editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='article',
            name='stock_updated',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 9, 10, 3, 5, 421635, tzinfo=utc), verbose_name='stock updated at', editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='article',
            name='stock_value_updated',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 9, 10, 3, 5, 421777, tzinfo=utc), verbose_name='stock value updated at', editable=False),
            preserve_default=True,
        ),
    ]
