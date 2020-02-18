# Generated by Django 2.1.5 on 2020-02-18 17:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('choonz', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('webpage', models.URLField(blank=True)),
                ('linkToSpotify', models.URLField(blank=True)),
                ('numberOfPlaylists', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stars', models.IntegerField(default=0)),
                ('comment', models.CharField(max_length=256)),
                ('date', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('linkToSpotify', models.URLField(blank=True)),
                ('numberOfPlaylists', models.IntegerField(default=0)),
                ('linkOther', models.URLField(blank=True)),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='choonz.Artist')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=30)),
                ('numberOfPlaylists', models.IntegerField(default=0)),
            ],
        ),
        migrations.RemoveField(
            model_name='page',
            name='playlist',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='website',
        ),
        migrations.AddField(
            model_name='playlist',
            name='averageRating',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='playlist',
            name='createdDate',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='playlist',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='playlist',
            name='description',
            field=models.CharField(default='Description...', max_length=256),
        ),
        migrations.AddField(
            model_name='playlist',
            name='image',
            field=models.FileField(blank=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='playlist',
            name='lastUpdatedDate',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='playlist',
            name='numberOfRatings',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='playlist',
            name='public',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='playlist',
            name='songs',
            field=models.ManyToManyField(related_name='_playlist_songs_+', to='choonz.Playlist'),
        ),
        migrations.DeleteModel(
            name='Page',
        ),
        migrations.AddField(
            model_name='rating',
            name='playlist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='choonz.Playlist'),
        ),
        migrations.AddField(
            model_name='rating',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='playlist',
            name='tags',
            field=models.ManyToManyField(to='choonz.Tag'),
        ),
    ]
