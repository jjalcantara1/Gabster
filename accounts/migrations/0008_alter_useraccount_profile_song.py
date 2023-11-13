# Generated by Django 4.2.4 on 2023-10-31 07:16

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_alter_useraccount_backgroundcolor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='profile_song',
            field=models.FileField(blank=True, default=None, null=True, upload_to=accounts.models.get_profile_song_filepath),
        ),
    ]
