# Generated by Django 2.1.15 on 2020-04-04 20:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0013_auto_20200404_2005'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pocketcastssettings',
            name='profile',
        ),
        migrations.DeleteModel(
            name='PocketCastsSettings',
        ),
    ]