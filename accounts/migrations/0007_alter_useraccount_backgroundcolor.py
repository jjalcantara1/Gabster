# Generated by Django 4.2.4 on 2023-10-27 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_useraccount_backgroundcolor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='backgroundColor',
            field=models.TextField(default='linear-gradient(to right, rgba(88,44,4,0.9), rgba(44,22,5, 0.9))'),
        ),
    ]
