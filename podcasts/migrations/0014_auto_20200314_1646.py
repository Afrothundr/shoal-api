# Generated by Django 2.1.15 on 2020-03-14 16:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('podcasts', '0013_auto_20200117_2215'),
    ]

    operations = [
        migrations.RenameField(
            model_name='like',
            old_name='comment',
            new_name='commentz',
        ),
    ]
