# Generated by Django 2.1.5 on 2020-03-08 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('choonz', '0003_auto_20200308_2259'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='numberOfPlaylists',
            field=models.IntegerField(default=0),
        ),
    ]