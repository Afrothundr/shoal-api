# Generated by Django 2.1.15 on 2020-01-08 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('podcasts', '0010_auto_20200107_2307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='podcast',
            name='podcast_id',
            field=models.TextField(default='0', max_length=256, unique=True),
        ),
    ]
