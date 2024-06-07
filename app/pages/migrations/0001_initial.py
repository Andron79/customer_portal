# Generated by Django 4.0.4 on 2022-05-24 09:23

import ckeditor_uploader.fields
from django.db import migrations, models
import pages.fields
import pages.yandex_s3_storage


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customer_dashboard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('title', models.CharField(max_length=250, unique=True, verbose_name='Title')),
                ('company_types', models.ManyToManyField(blank=True, to='customer_dashboard.companytype', verbose_name='Company types')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
        ),
        migrations.CreateModel(
            name='Tutorial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('title', models.CharField(max_length=250, unique=True, verbose_name='Title')),
                ('description', models.TextField(blank=True, max_length=2500, null=True, verbose_name='Description')),
                ('is_public', models.BooleanField(default=False, verbose_name='Display in Public Page')),
                ('image', models.ImageField(upload_to='images/')),
                ('external_url', models.URLField(verbose_name='External URL')),
                ('company', models.ManyToManyField(blank=True, to='customer_dashboard.company', verbose_name='Companies')),
                ('product', models.ManyToManyField(blank=True, to='pages.product', verbose_name='Products')),
            ],
            options={
                'verbose_name': 'Tutorial',
                'verbose_name_plural': 'Tutorials',
            },
        ),
        migrations.CreateModel(
            name='Information',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('title', models.CharField(max_length=250, unique=True, verbose_name='Title')),
                ('is_public', models.BooleanField(default=False, verbose_name='Display in Public Page')),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Description')),
                ('company', models.ManyToManyField(blank=True, to='customer_dashboard.company', verbose_name='Companies')),
                ('product', models.ManyToManyField(blank=True, to='pages.product', verbose_name='Products')),
            ],
            options={
                'verbose_name': 'Information',
                'verbose_name_plural': "Information's",
            },
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('title', models.CharField(max_length=250, unique=True, verbose_name='Title')),
                ('description', models.TextField(blank=True, max_length=2500, null=True, verbose_name='Description')),
                ('is_public', models.BooleanField(default=False, verbose_name='Display in Public Page')),
                ('file', pages.fields.PrivateFileField(storage=pages.yandex_s3_storage.PrivateClientUserContentStorage(), upload_to='Files', verbose_name='file')),
                ('company', models.ManyToManyField(blank=True, to='customer_dashboard.company', verbose_name='Companies')),
                ('product', models.ManyToManyField(blank=True, to='pages.product', verbose_name='Products')),
            ],
            options={
                'verbose_name': 'File',
                'verbose_name_plural': 'Files',
            },
        ),
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('question', models.CharField(max_length=500, verbose_name='Question')),
                ('answer', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Answer')),
                ('is_public', models.BooleanField(default=False, verbose_name='Display in Public Page')),
                ('company', models.ManyToManyField(blank=True, to='customer_dashboard.company', verbose_name='Companies')),
                ('product', models.ManyToManyField(blank=True, to='pages.product', verbose_name='Products')),
            ],
            options={
                'verbose_name': 'FAQ',
                'verbose_name_plural': 'FAQs',
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('title', models.CharField(max_length=250, unique=True, verbose_name='Title')),
                ('description', models.TextField(blank=True, max_length=2500, null=True, verbose_name='Description')),
                ('is_public', models.BooleanField(default=False, verbose_name='Display in Public Page')),
                ('file', pages.fields.PrivateFileField(storage=pages.yandex_s3_storage.PrivateClientUserContentStorage(), upload_to='Documents', verbose_name='file')),
                ('company', models.ManyToManyField(blank=True, to='customer_dashboard.company', verbose_name='Companies')),
                ('product', models.ManyToManyField(blank=True, to='pages.product', verbose_name='Products')),
            ],
            options={
                'verbose_name': 'Document',
                'verbose_name_plural': 'Documents',
            },
        ),
    ]
