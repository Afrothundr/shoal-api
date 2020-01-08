# Generated by Django 2.1.15 on 2020-01-07 23:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('podcasts', '0009_auto_20200102_2003'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='podcast_id',
        ),
        migrations.RemoveField(
            model_name='podcast',
            name='author',
        ),
        migrations.RemoveField(
            model_name='podcast',
            name='categories',
        ),
        migrations.RemoveField(
            model_name='podcast',
            name='description',
        ),
        migrations.RemoveField(
            model_name='podcast',
            name='episodesSortOrder',
        ),
        migrations.RemoveField(
            model_name='podcast',
            name='language',
        ),
        migrations.RemoveField(
            model_name='podcast',
            name='mediatype',
        ),
        migrations.RemoveField(
            model_name='podcast',
            name='thumbnailSmall',
        ),
        migrations.RemoveField(
            model_name='podcast',
            name='thumbnailurl',
        ),
        migrations.RemoveField(
            model_name='podcast',
            name='title',
        ),
        migrations.RemoveField(
            model_name='podcast',
            name='url',
        ),
        migrations.AddField(
            model_name='comment',
            name='podcast',
            field=models.ForeignKey(default='0', on_delete=django.db.models.deletion.DO_NOTHING, related_name='comments', to='podcasts.Podcast'),
        ),
        migrations.AddField(
            model_name='podcast',
            name='podcast_id',
            field=models.TextField(default='0', max_length=256),
        ),
    ]