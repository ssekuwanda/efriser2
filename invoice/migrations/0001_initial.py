# Generated by Django 4.0.3 on 2022-10-21 15:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BarCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('barcode', models.ImageField(blank=True, null=True, upload_to='')),
                ('date_created', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('business_name', models.CharField(max_length=100, null=True)),
                ('address', models.CharField(max_length=10000, null=True)),
                ('email_address', models.EmailField(max_length=254, null=True)),
                ('company_type', models.CharField(choices=[('0', 'Business'), ('3', 'Government'), ('1', 'Consumer'), ('2', 'Foreigner')], max_length=100, null=True)),
                ('contact_number', models.CharField(max_length=100, null=True)),
                ('tin', models.CharField(blank=True, help_text='leave blank if export', max_length=10, null=True)),
                ('uniqueId', models.CharField(blank=True, max_length=100, null=True)),
                ('slug', models.SlugField(blank=True, max_length=500, null=True, unique=True)),
                ('date_created', models.DateTimeField(blank=True, null=True)),
                ('last_updated', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Company Name')),
                ('short_name', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=1000)),
                ('telephone_number', models.CharField(max_length=100)),
                ('location', models.CharField(help_text='Separate Each location Detail with >', max_length=1000)),
                ('website', models.CharField(blank=True, max_length=1001)),
                ('companyLogo', models.ImageField(default='default_logo.jpg', null=True, upload_to='company_logos', verbose_name='Logo')),
                ('tin', models.CharField(max_length=10)),
                ('device_number', models.CharField(help_text='TCSc0192929020020', max_length=100)),
                ('url', models.URLField(help_text='http://167.109.66.192:9880/efristcs/ws/tcsapp/getInformation', null=True)),
                ('wht_exempt', models.BooleanField(default=False)),
                ('vat_wht', models.BooleanField(default=False)),
                ('nature', models.CharField(choices=[('Services', 'Services'), ('Products', 'Products')], max_length=120)),
                ('slug', models.SlugField(blank=True, max_length=500, null=True, unique=True)),
                ('date_created', models.DateTimeField(blank=True, null=True)),
                ('last_updated', models.DateTimeField(blank=True, null=True)),
                ('owner', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='company1', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('finalized', models.BooleanField(default=False)),
                ('remarks', models.TextField(max_length=1000, null=True)),
                ('currency', models.CharField(choices=[('UGX', 'UGX'), ('USD', 'USD'), ('GBP', 'GBP')], max_length=100, null=True, verbose_name='CURRENCY')),
                ('tax', models.CharField(max_length=100, null=True)),
                ('payment_method', models.CharField(choices=[('107', 'EFT'), ('106', 'Visa'), ('105', 'Mobile money'), ('103', 'Cheque'), ('102', 'Cash'), ('101', 'Credit')], max_length=100, null=True)),
                ('fdn', models.CharField(blank=True, max_length=100, null=True)),
                ('json_response', jsonfield.fields.JSONField(blank=True)),
                ('uniqueId', models.CharField(blank=True, max_length=100, null=True)),
                ('slug', models.SlugField(blank=True, max_length=500, null=True, unique=True)),
                ('date_created', models.DateTimeField(blank=True, null=True)),
                ('last_updated', models.DateTimeField(blank=True, null=True)),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='invoice.client')),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='invoice.company')),
            ],
            options={
                'ordering': ('-date_created',),
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(help_text='The code should be unique to all produucts', max_length=40)),
                ('unit_price', models.FloatField(default=1, verbose_name='Unit Price')),
                ('currency', models.CharField(choices=[('UGX', 'UGX'), ('USD', 'USD'), ('GBP', 'GBP')], max_length=3)),
                ('tax_rate', models.CharField(choices=[('18%', 'Standard Rated Sale'), ('-', 'Export'), ('0%', 'Exempt')], default='18%', max_length=3)),
                ('commodity_id', models.CharField(help_text='An 18 digit code from URA coding system', max_length=18)),
                ('has_excise_duty', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=3, null=True)),
                ('description', models.CharField(max_length=1024, null=True)),
                ('stock_warning', models.CharField(max_length=24)),
                ('uniqueId', models.CharField(blank=True, max_length=100, null=True)),
                ('slug', models.TextField(blank=True, null=True, unique=True)),
                ('date_created', models.DateTimeField(blank=True, null=True)),
                ('last_updated', models.DateTimeField(blank=True, null=True)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='invoice.company')),
            ],
            options={
                'ordering': ('-date_created',),
            },
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clientName', models.CharField(blank=True, max_length=200, null=True)),
                ('clientLogo', models.ImageField(default='default_logo.jpg', upload_to='company_logos')),
                ('addressLine1', models.CharField(blank=True, max_length=200, null=True)),
                ('postalCode', models.CharField(blank=True, max_length=10, null=True)),
                ('phoneNumber', models.CharField(blank=True, max_length=100, null=True)),
                ('emailAddress', models.CharField(blank=True, max_length=100, null=True)),
                ('taxNumber', models.CharField(blank=True, max_length=100, null=True)),
                ('uniqueId', models.CharField(blank=True, max_length=100, null=True)),
                ('slug', models.SlugField(blank=True, max_length=500, null=True, unique=True)),
                ('date_created', models.DateTimeField(blank=True, null=True)),
                ('last_updated', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tax_Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=2)),
                ('description', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Unit_Measurement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=3, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductMeta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock', models.PositiveIntegerField(null=True)),
                ('price', models.PositiveIntegerField(null=True)),
                ('date_created', models.DateTimeField(blank=True, null=True)),
                ('last_updated', models.DateTimeField(blank=True, null=True)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='invoice.company')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prod_meta', to='invoice.product')),
            ],
            options={
                'ordering': ('-date_created',),
            },
        ),
        migrations.AddField(
            model_name='product',
            name='unit_measure',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='invoice.unit_measurement'),
        ),
        migrations.CreateModel(
            name='InvoiceProducts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', models.TextField(blank=True, null=True)),
                ('quantity', models.FloatField(blank=True, default=1)),
                ('vat', models.CharField(choices=[('18%', 'Standard Rated Sale'), ('-', 'Export'), ('0%', 'Exempt')], max_length=100, null=True, verbose_name='VAT')),
                ('price', models.FloatField(verbose_name='Unit Price')),
                ('uniqueId', models.CharField(blank=True, max_length=100, null=True)),
                ('slug', models.SlugField(blank=True, max_length=500, null=True, unique=True)),
                ('date_created', models.DateTimeField(auto_now=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now_add=True)),
                ('invoice', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='inv_prod', to='invoice.invoice')),
                ('product', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='invoice.product')),
                ('tax_type', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='invoice.tax_type')),
            ],
            options={
                'ordering': ('-date_created',),
            },
        ),
        migrations.CreateModel(
            name='CreditNote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('reason_code', models.CharField(choices=[('101', 'Return of products due to expiry or damage, etc.'), ('102', 'Cancellation of the purchase'), ('103', 'Invoice amount wrongly stated due to miscalculation of price, tax or discounts, etc.'), ('104', 'Partial or complete waive off of the service sale after the invoice is generated and sent to the customer'), ('105', 'Others (Please specify')], max_length=10000)),
                ('json_response', models.TextField(null=True)),
                ('reason', models.TextField(null=True)),
                ('anti_fake', models.CharField(blank=True, max_length=10000, null=True)),
                ('reference', models.CharField(max_length=10000, null=True)),
                ('status', models.BooleanField(default=False)),
                ('fdn', models.CharField(blank=True, max_length=122, null=True)),
                ('approval', models.CharField(default='Pending', max_length=122, null=True)),
                ('number', models.IntegerField()),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='invoice.company')),
                ('invoice', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='credit_notes', to='invoice.invoice')),
            ],
            options={
                'ordering': ('-date_created',),
            },
        ),
        migrations.CreateModel(
            name='CompanyLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plot', models.CharField(max_length=1000, null=True)),
                ('pobox', models.CharField(max_length=1000, null=True, verbose_name='P.O.Box')),
                ('location', models.CharField(default='Kampala, Uganda', max_length=1000, null=True)),
                ('other_details', models.CharField(max_length=1000, null=True)),
                ('company', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='invoice.company')),
            ],
        ),
        migrations.CreateModel(
            name='CnCancel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(choices=[('101', 'Buyer refused to accept the invoice due to incorrect invoice/receipt'), ('102', 'Not delivered due to incorrect invoice/receipt'), ('103', 'Other reasons')], max_length=10000, null=True)),
                ('details', models.CharField(blank=True, max_length=100, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('cn', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='invoice.creditnote')),
            ],
            options={
                'ordering': ('-date_created',),
            },
        ),
        migrations.AddField(
            model_name='client',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='invoice.company'),
        ),
        migrations.CreateModel(
            name='BankDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_name', models.CharField(max_length=1000)),
                ('branch', models.CharField(max_length=1000)),
                ('account_name', models.CharField(max_length=1000)),
                ('account_number', models.BigIntegerField()),
                ('swift_address', models.CharField(max_length=1000)),
                ('swift_code', models.CharField(max_length=1000)),
                ('currency', models.CharField(choices=[('UGX', 'UGX'), ('USD', 'USD'), ('GBP', 'GBP')], max_length=1000)),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bank_details', to='invoice.company')),
            ],
        ),
    ]
