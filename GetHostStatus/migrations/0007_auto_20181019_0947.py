# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GetHostStatus', '0006_auto_20181019_0015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historydata',
            name='type',
            field=models.CharField(max_length=32, verbose_name=b'type', choices=[(b'N', '\u7acb\u523b\u68c0\u67e5'), (b'A', '\u52a0\u5165\u81ea\u52a8\u68c0\u67e5'), (b'D', '\u79fb\u9664\u81ea\u52a8\u68c0\u67e5')]),
        ),
    ]
