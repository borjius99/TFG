# Generated by Django 2.2.12 on 2022-06-29 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FakeApp', '0002_userprofile_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='public_key',
            field=models.CharField(max_length=700),
        ),
    ]
