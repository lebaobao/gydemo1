# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('GetHostStatus', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cpudata',
            old_name='creat_time',
            new_name='creattime',
        ),
        migrations.RemoveField(
            model_name='cpudata',
            name='check_date',
        ),
        migrations.AddField(
            model_name='cpudata',
            name='checkdate',
            field=models.CharField(default=datetime.datetime(2018, 10, 17, 10, 0, 29, 109000), max_length=128, verbose_name=b'check_date'),
            preserve_default=False,
        ),
    ]
