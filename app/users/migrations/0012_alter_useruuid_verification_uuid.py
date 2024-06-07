# Generated by Django 4.0.4 on 2022-10-04 11:44

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_alter_customuser_is_active_useruuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useruuid',
            name='verification_uuid',
            field=models.UUIDField(default=uuid.uuid4, null=True, verbose_name='User UUID'),
        ),
    ]
