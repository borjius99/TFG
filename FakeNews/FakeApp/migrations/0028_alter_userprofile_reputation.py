# Generated by Django 4.0.6 on 2022-08-02 09:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FakeApp', '0027_news_legitima'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='reputation',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(-2)]),
        ),
    ]