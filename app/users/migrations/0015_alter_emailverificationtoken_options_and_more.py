# Generated by Django 4.0.4 on 2022-10-10 15:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_rename_useruuid_emailverificationtoken'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='emailverificationtoken',
            options={'verbose_name': 'Token', 'verbose_name_plural': 'Tokens'},
        ),
        migrations.AlterField(
            model_name='emailverificationtoken',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='email_verification_token', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='emailverificationtoken',
            name='verification_uuid',
            field=models.UUIDField(default=uuid.uuid4, null=True, verbose_name='Token'),
        ),
    ]
