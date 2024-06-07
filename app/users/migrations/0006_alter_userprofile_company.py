# Generated by Django 4.0.4 on 2022-05-31 12:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer_dashboard', '0002_alter_company_created_at_alter_company_updated_at'),
        ('users', '0005_alter_userprofile_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='customer_dashboard.company', verbose_name='Company'),
        ),
    ]