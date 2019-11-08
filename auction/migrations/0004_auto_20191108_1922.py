# Generated by Django 2.2.5 on 2019-11-08 17:22

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auction', '0003_auto_20191107_2311'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction_list',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_auction', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='auction_list',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 11, 17, 22, 48, 288614, tzinfo=utc)),
        ),
    ]
