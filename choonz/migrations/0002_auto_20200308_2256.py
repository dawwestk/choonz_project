# Generated by Django 2.1.5 on 2020-03-08 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('choonz', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='webpage',
            field=models.URLField(blank=True, null=True),
        ),
    ]