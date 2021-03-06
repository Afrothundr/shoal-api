# Generated by Django 2.1.15 on 2019-12-31 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_auto_20191231_1639'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='friends',
            field=models.ManyToManyField(related_name='_profile_friends_+', to='profiles.Profile'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='podcasts',
            field=models.ManyToManyField(to='podcasts.Podcast'),
        ),
    ]
