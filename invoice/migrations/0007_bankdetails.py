# Generated by Django 4.0.5 on 2022-06-23 08:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0006_company_wht_exempt'),
    ]

    operations = [
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
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='invoice.company')),
            ],
        ),
    ]
