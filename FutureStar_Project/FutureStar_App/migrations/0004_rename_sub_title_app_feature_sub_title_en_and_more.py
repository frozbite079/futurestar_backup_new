# Generated by Django 5.0 on 2024-09-19 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FutureStar_App', '0003_rename_designations_team_members_designations_en_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='app_feature',
            old_name='sub_title',
            new_name='sub_title_en',
        ),
        migrations.RenameField(
            model_name='app_feature',
            old_name='title',
            new_name='title_en',
        ),
        migrations.AddField(
            model_name='app_feature',
            name='sub_title_ar',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='app_feature',
            name='title_ar',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
