# Generated by Django 2.2.5 on 2019-11-08 22:46

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0005_auto_20191109_0042'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auction_list',
            name='posted',
        ),
        migrations.AlterField(
            model_name='auction_list',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 11, 22, 46, 7, 574550, tzinfo=utc)),
        ),
    ]
