# Generated by Django 4.0.4 on 2022-12-07 14:27

import customer_dashboard.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer_dashboard', '0003_company_max_num_company_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='inn',
            field=models.CharField(max_length=12, null=True, validators=[customer_dashboard.validators.validate_digit], verbose_name='INN'),
        ),
        migrations.AddField(
            model_name='company',
            name='kpp',
            field=models.CharField(max_length=9, null=True, validators=[customer_dashboard.validators.validate_digit], verbose_name='KPP'),
        ),
        migrations.AddConstraint(
            model_name='company',
            constraint=models.UniqueConstraint(fields=('inn', 'kpp'), name='uniq_company_key'),
        ),
    ]
