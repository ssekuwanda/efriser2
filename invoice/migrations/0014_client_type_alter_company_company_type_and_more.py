# Generated by Django 4.0.5 on 2022-07-01 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0013_creditnote_company_alter_creditnote_reason_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='company_type',
            field=models.CharField(choices=[('B2B', 'Business'), ('B2G', 'Government'), ('B2C', 'Consumer'), ('B2F', 'Foreigner')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='payment_method',
            field=models.CharField(blank=True, choices=[('107', 'EFT'), ('106', 'Visa'), ('105', 'Mobile money'), ('103', 'Cheque'), ('102', 'Cash'), ('101', 'Credit')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='invoiceproducts',
            name='quantity',
            field=models.FloatField(blank=True, default=1),
        ),
        migrations.AlterField(
            model_name='product',
            name='tax_rate',
            field=models.CharField(choices=[('18%', 'Standard Rated Sale'), ('0%', 'Export'), ('0%', 'Exempt')], default='18%', max_length=3),
        ),
        migrations.AlterField(
            model_name='product',
            name='unit_price',
            field=models.FloatField(blank=True, default=1, verbose_name='Fees'),
        ),
    ]
