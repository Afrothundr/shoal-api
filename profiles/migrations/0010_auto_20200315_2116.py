# Generated by Django 2.1.15 on 2020-03-15 21:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0009_profile_body'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='body',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='pcsettings',
        ),
        migrations.AddField(
            model_name='pocketcastssettings',
            name='p',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, related_name='p', to='profiles.Profile'),
        ),
    ]
