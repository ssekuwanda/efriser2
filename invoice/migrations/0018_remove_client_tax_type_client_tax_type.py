# Generated by Django 4.0.5 on 2022-07-06 15:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0017_tax_type_alter_invoice_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='tax_type',
        ),
        migrations.AddField(
            model_name='client',
            name='tax_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='invoice.tax_type'),
            preserve_default=False,
        ),
    ]
