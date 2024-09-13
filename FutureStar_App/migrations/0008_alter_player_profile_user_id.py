# Generated by Django 5.1.1 on 2024-09-12 04:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FutureStar_App', '0007_alter_player_profile_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player_profile',
            name='user_id',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player_profile', to=settings.AUTH_USER_MODEL),
        ),
    ]