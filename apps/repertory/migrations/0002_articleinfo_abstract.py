# Generated by Django 2.1 on 2018-11-05 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repertory', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='articleinfo',
            name='abstract',
            field=models.CharField(default='safa', max_length=200),
            preserve_default=False,
        ),
    ]
