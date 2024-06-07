# Generated by Django 4.0.4 on 2022-10-04 10:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_alter_userprofile_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='Is active'),
        ),
        migrations.CreateModel(
            name='UserUuid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('verification_uuid', models.UUIDField(default=uuid.uuid4, null=True, unique=True, verbose_name='User UUID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_uuid', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User UUID',
                'verbose_name_plural': 'Users UUIDs',
            },
        ),
    ]