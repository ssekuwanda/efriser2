# Generated by Django 4.0.5 on 2022-07-26 09:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0024_company_comp_url'),
    ]

    operations = [
        migrations.RenameField(
            model_name='company',
            old_name='comp_url',
            new_name='url',
        ),
    ]
