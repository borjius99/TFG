# Generated by Django 4.0.6 on 2022-07-21 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FakeApp', '0024_alter_news_voters'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='visualizations',
            field=models.IntegerField(default=0),
        ),
    ]
