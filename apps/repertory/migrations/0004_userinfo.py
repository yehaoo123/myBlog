# Generated by Django 2.1 on 2018-11-07 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repertory', '0003_auto_20181105_1252'),
    ]

    operations = [
        migrations.CreateModel(
            name='userInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=22)),
                ('password', models.CharField(max_length=32)),
            ],
        ),
    ]
