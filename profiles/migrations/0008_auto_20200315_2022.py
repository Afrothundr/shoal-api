# Generated by Django 2.1.15 on 2020-03-15 20:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0007_auto_20200314_1714'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='pocket_cast_settings',
            new_name='pcsettings',
        ),
    ]
