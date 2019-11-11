# Generated by Django 2.2.5 on 2019-11-11 19:42

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auction', '0009_auto_20191111_0959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction_list',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 14, 19, 42, 5, 830489, tzinfo=utc)),
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_pref', models.CharField(max_length=5, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bidprice', models.DecimalField(decimal_places=2, max_digits=10)),
                ('itemid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auction.Auction_list')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
