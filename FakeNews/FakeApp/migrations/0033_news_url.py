# Generated by Django 4.0.6 on 2022-08-09 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FakeApp', '0032_userprofile_canpublish'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='url',
            field=models.URLField(default=''),
        ),
    ]
