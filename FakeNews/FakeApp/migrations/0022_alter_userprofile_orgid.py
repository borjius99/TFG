# Generated by Django 4.0.6 on 2022-07-15 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FakeApp', '0021_alter_userprofile_orgid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='orgId',
            field=models.IntegerField(blank=True, unique=True),
        ),
    ]
