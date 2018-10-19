# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GetHostStatus', '0005_auto_20181018_2300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historydata',
            name='ip',
            field=models.CharField(max_length=64, verbose_name=b'ip'),
        ),
    ]
