# Generated by Django 4.0.4 on 2022-05-30 13:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer_dashboard', '0002_alter_company_created_at_alter_company_updated_at'),
        ('users', '0002_alter_userprofile_company_alter_userprofile_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='company',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='customer_dashboard.company', verbose_name='Company'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='role',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Company Admin'), (2, 'Company Employee')], default=1),
        ),
    ]