# Generated by Django 2.2.12 on 2022-07-06 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FakeApp', '0006_news'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='public_key',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='org_source',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='reputation',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='org_name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='wallet',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
