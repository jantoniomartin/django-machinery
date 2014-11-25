# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('wm', '0002_article_weight'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='stock_updated',
            field=models.DateTimeField(default=datetime.datetime(2014, 11, 24, 8, 30, 43, 679628, tzinfo=utc), verbose_name='stock updated at'),
            preserve_default=True,
        ),
    ]
