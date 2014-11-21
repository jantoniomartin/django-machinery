# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wm', '0001_initial'),
        ('crm', '0001_initial'),
        ('om', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='article',
            field=models.ForeignKey(verbose_name='article', to='wm.Article'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='offer',
            name='company',
            field=models.ForeignKey(verbose_name='company', to='crm.Company'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='csvtemplate',
            name='company',
            field=models.ForeignKey(verbose_name='company', to='crm.Company'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cartitem',
            name='offer',
            field=models.ForeignKey(verbose_name='offer', to='om.Offer'),
            preserve_default=True,
        ),
    ]
