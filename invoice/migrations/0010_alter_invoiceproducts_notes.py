# Generated by Django 4.0.5 on 2022-06-08 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0009_alter_invoiceproducts_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoiceproducts',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
    ]
