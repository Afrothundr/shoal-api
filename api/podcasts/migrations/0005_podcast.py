# Generated by Django 2.1.4 on 2019-12-05 22:19

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('podcasts', '0004_delete_podcast'),
    ]

    operations = [
        migrations.CreateModel(
            name='Podcast',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256, unique=True)),
                ('author', models.CharField(max_length=256)),
                ('description', models.TextField(blank=True)),
                ('url', models.URLField()),
                ('episodesSortOrder', models.IntegerField()),
                ('language', models.CharField(max_length=64)),
                ('categories', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=48), size=None)),
                ('thumbnailurl', models.URLField(blank=True)),
                ('thumbnailSmall', models.URLField(blank=True)),
                ('mediatype', models.URLField(blank=True)),
            ],
        ),
    ]
