# Generated by Django 3.1.4 on 2020-12-21 04:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0020_auto_20201103_0211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pocketcastssettings',
            name='email',
            field=models.TextField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='pocketcastssettings',
            name='password',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='pocketcastssettings',
            name='profile',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='pocketcasts_settings', to='profiles.profile'),
        ),
    ]
