# Generated by Django 4.0.6 on 2022-07-15 09:51

import FakeApp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FakeApp', '0016_alter_news_voters'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='voters',
            field=models.JSONField(default=FakeApp.models.voters_default),
        ),
    ]
