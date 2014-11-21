# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='name')),
                ('vatin', models.CharField(max_length=16, null=True, verbose_name='VATIN', blank=True)),
                ('address', models.CharField(max_length=255, null=True, verbose_name='address', blank=True)),
                ('city', models.CharField(max_length=50, null=True, verbose_name='city', blank=True)),
                ('region', models.CharField(max_length=50, null=True, verbose_name='region', blank=True)),
                ('postal_code', models.CharField(max_length=10, null=True, verbose_name='postal code', blank=True)),
                ('country', models.CharField(max_length=50, null=True, verbose_name='country', blank=True)),
                ('comment', models.TextField(null=True, verbose_name='comment', blank=True)),
                ('website', models.URLField(null=True, verbose_name='website', blank=True)),
                ('global_email', models.EmailField(max_length=75, null=True, verbose_name='global email', blank=True)),
                ('main_phone', models.CharField(max_length=40, null=True, verbose_name='main phone', blank=True)),
                ('secondary_phone', models.CharField(max_length=40, null=True, verbose_name='secondary_phone', blank=True)),
                ('fax', models.CharField(max_length=40, null=True, verbose_name='fax', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('is_customer', models.BooleanField(default=False, verbose_name=' is customer')),
                ('is_supplier', models.BooleanField(default=False, verbose_name=' is supplier')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'company',
                'verbose_name_plural': 'companies',
                'permissions': (('view_company', 'Can view company'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language', models.CharField(max_length=8, verbose_name='language', choices=[(b'en', b'Ingl\xc3\xa9s'), (b'es', b'Espa\xc3\xb1ol')])),
                ('disaggregated', models.BooleanField(default=True, verbose_name='disaggregated')),
                ('total', models.DecimalField(null=True, verbose_name='total', max_digits=12, decimal_places=2, blank=True)),
                ('created', models.DateField(verbose_name='created')),
                ('delivery_time', models.TextField(default=b'', verbose_name='delivery time', blank=True)),
                ('delivery_method', models.CharField(default=b'', max_length=255, verbose_name='delivery method', blank=True)),
                ('conditions', models.TextField(default=b'', verbose_name='conditions', blank=True)),
                ('remarks', models.TextField(default=b'', verbose_name='remarks', blank=True)),
                ('vat', models.DecimalField(verbose_name='VAT', max_digits=4, decimal_places=2, choices=[(Decimal('0.00'), b'0%'), (Decimal('21.00'), b'21%')])),
                ('signed_copy', models.FileField(upload_to=b'crm/contracts', null=True, verbose_name='signed copy', blank=True)),
                ('author', models.ForeignKey(verbose_name='author', to=settings.AUTH_USER_MODEL)),
                ('company', models.ForeignKey(verbose_name='company', to='crm.Company')),
            ],
            options={
                'ordering': ['-id'],
                'abstract': False,
                'verbose_name': 'contract',
                'verbose_name_plural': 'contracts',
                'permissions': (('view_contract', 'Can view contract'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ContractItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='quantity')),
                ('description', models.TextField(verbose_name='description')),
                ('price', models.DecimalField(null=True, verbose_name='price', max_digits=12, decimal_places=2, blank=True)),
                ('contract', models.ForeignKey(verbose_name='contract', to='crm.Contract')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'contract item',
                'verbose_name_plural': 'contract items',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DeliveryNote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateField(auto_now_add=True, verbose_name='created')),
                ('remarks', models.TextField(default=b'', verbose_name='remarks', blank=True)),
                ('contract', models.ForeignKey(verbose_name='contract', to='crm.Contract')),
            ],
            options={
                'ordering': ['-id'],
                'verbose_name': 'delivery note',
                'verbose_name_plural': 'delivery notes',
                'permissions': (('view_deliverynote', 'Can view delivery note'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DeliveryNoteItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='quantity')),
                ('description', models.TextField(verbose_name='description')),
                ('note', models.ForeignKey(verbose_name='delivery note', to='crm.DeliveryNote')),
            ],
            options={
                'verbose_name': 'delivery note item',
                'verbose_name_plural': 'delivery note items',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('person', models.CharField(max_length=100, null=True, verbose_name='person', blank=True)),
                ('phone', models.CharField(max_length=40, null=True, verbose_name='phone', blank=True)),
                ('email', models.EmailField(max_length=75, null=True, verbose_name='email', blank=True)),
                ('send_orders', models.BooleanField(default=False, verbose_name='send orders')),
                ('comment', models.CharField(max_length=255, null=True, verbose_name='comment', blank=True)),
                ('company', models.ForeignKey(verbose_name='company', blank=True, to='crm.Company', null=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'department',
                'verbose_name_plural': 'departments',
                'permissions': (('view_department', 'Can view department'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50, verbose_name='name')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'group',
                'verbose_name_plural': 'groups',
                'permissions': (('view_group', 'Can view group'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Proforma',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language', models.CharField(max_length=8, verbose_name='language', choices=[(b'en', b'Ingl\xc3\xa9s'), (b'es', b'Espa\xc3\xb1ol')])),
                ('disaggregated', models.BooleanField(default=True, verbose_name='disaggregated')),
                ('total', models.DecimalField(null=True, verbose_name='total', max_digits=12, decimal_places=2, blank=True)),
                ('created', models.DateField(verbose_name='created')),
                ('remarks', models.TextField(default=b'', verbose_name='remarks', blank=True)),
                ('vat', models.DecimalField(verbose_name='VAT', max_digits=4, decimal_places=2, choices=[(Decimal('0.00'), b'0%'), (Decimal('21.00'), b'21%')])),
                ('author', models.ForeignKey(verbose_name='author', to=settings.AUTH_USER_MODEL)),
                ('company', models.ForeignKey(verbose_name='company', to='crm.Company')),
            ],
            options={
                'ordering': ['-id'],
                'abstract': False,
                'verbose_name': 'proforma',
                'verbose_name_plural': 'proformas',
                'permissions': (('view_proforma', 'Can view proforma'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProformaItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='quantity')),
                ('description', models.TextField(verbose_name='description')),
                ('price', models.DecimalField(null=True, verbose_name='price', max_digits=12, decimal_places=2, blank=True)),
                ('proforma', models.ForeignKey(verbose_name='proforma', to='crm.Proforma')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'proforma item',
                'verbose_name_plural': 'proforma items',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Quotation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language', models.CharField(max_length=8, verbose_name='language', choices=[(b'en', b'Ingl\xc3\xa9s'), (b'es', b'Espa\xc3\xb1ol')])),
                ('disaggregated', models.BooleanField(default=True, verbose_name='disaggregated')),
                ('total', models.DecimalField(null=True, verbose_name='total', max_digits=12, decimal_places=2, blank=True)),
                ('created', models.DateField(auto_now_add=True, verbose_name='created')),
                ('recipient_name', models.CharField(max_length=255, null=True, verbose_name='recipient name', blank=True)),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('conditions', models.TextField(null=True, verbose_name='conditions', blank=True)),
                ('private_note', models.CharField(max_length=255, null=True, verbose_name='private note', blank=True)),
                ('author', models.ForeignKey(verbose_name='author', to=settings.AUTH_USER_MODEL)),
                ('company', models.ForeignKey(verbose_name='company', to='crm.Company')),
            ],
            options={
                'ordering': ['-id'],
                'abstract': False,
                'verbose_name': 'quotation',
                'verbose_name_plural': 'quotations',
                'permissions': (('view_quotation', 'Can view quotation'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QuotationItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='quantity')),
                ('description', models.TextField(verbose_name='description')),
                ('price', models.DecimalField(null=True, verbose_name='price', max_digits=12, decimal_places=2, blank=True)),
                ('optional', models.BooleanField(default=False, verbose_name='optional')),
                ('quotation', models.ForeignKey(verbose_name='quotation', to='crm.Quotation')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'quotation item',
                'verbose_name_plural': 'quotation items',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='company',
            name='group',
            field=models.ForeignKey(verbose_name='group', blank=True, to='crm.Group', null=True),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
            ],
            options={
                'verbose_name': 'customer',
                'proxy': True,
                'verbose_name_plural': 'customers',
            },
            bases=('crm.company',),
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
            ],
            options={
                'verbose_name': 'supplier',
                'proxy': True,
                'verbose_name_plural': 'suppliers',
            },
            bases=('crm.company',),
        ),
    ]
