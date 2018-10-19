# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GetHostStatus', '0004_auto_20181018_2235'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='historydata',
            options={'verbose_name': 'historydata', 'verbose_name_plural': 'historydata'},
        ),
    ]
