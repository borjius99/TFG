# Generated by Django 4.0.6 on 2022-08-04 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FakeApp', '0028_alter_userprofile_reputation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='orgId',
            field=models.IntegerField(null=True, unique=True),
        ),
    ]
