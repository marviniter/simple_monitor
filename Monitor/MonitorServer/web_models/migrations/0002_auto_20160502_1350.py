# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('web_models', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cpu',
            name='clock',
            field=models.CharField(default=datetime.datetime(2016, 5, 2, 13, 50, 0, 677453, tzinfo=utc), max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='memory',
            name='clock',
            field=models.CharField(default=1, max_length=64),
            preserve_default=False,
        ),
    ]
