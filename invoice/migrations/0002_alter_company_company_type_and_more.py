# Generated by Django 4.0.5 on 2022-06-17 06:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='company_type',
            field=models.CharField(choices=[('Services', 'Services'), ('Products', 'Products')], default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='company',
            name='device_number',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='company',
            name='email',
            field=models.EmailField(default=1, max_length=1000),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(default=1, max_length=100, verbose_name='Company Name'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='company',
            name='tin',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='product',
            name='unit_measure',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='invoice.unit_measurement'),
        ),
        migrations.DeleteModel(
            name='ProductMeta',
        ),
    ]