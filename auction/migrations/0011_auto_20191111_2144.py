# Generated by Django 2.2.5 on 2019-11-11 19:44

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0010_auto_20191111_2142'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction_list',
            name='state',
            field=models.CharField(default='A', max_length=1),
        ),
        migrations.AlterField(
            model_name='auction_list',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 14, 19, 44, 22, 336230, tzinfo=utc)),
        ),
    ]
