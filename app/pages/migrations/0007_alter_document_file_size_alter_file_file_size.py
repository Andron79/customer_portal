# Generated by Django 4.0.4 on 2022-07-19 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0006_alter_document_file_size_alter_file_file_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='file_size',
            field=models.PositiveBigIntegerField(blank=True, null=True, verbose_name='File size'),
        ),
        migrations.AlterField(
            model_name='file',
            name='file_size',
            field=models.PositiveBigIntegerField(blank=True, null=True, verbose_name='File size'),
        ),
    ]