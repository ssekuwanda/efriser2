# Generated by Django 4.0.5 on 2022-06-23 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0005_invoiceproducts_vat'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='wht_exempt',
            field=models.BooleanField(default=False),
        ),
    ]
