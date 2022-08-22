# Generated by Django 4.0.5 on 2022-08-22 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0029_creditnote_number'),
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
        migrations.AlterField(
            model_name='company',
            name='device_number',
            field=models.CharField(help_text='TCSc0192929020020', max_length=100),
        ),
        migrations.AlterField(
            model_name='company',
            name='url',
            field=models.URLField(help_text='http://167.100.66.192:9880/efristcs/ws/tcsapp/getInformation', null=True),
        ),
        migrations.AlterField(
            model_name='creditnote',
            name='fdn',
            field=models.CharField(blank=True, max_length=122, null=True),
        ),
    ]