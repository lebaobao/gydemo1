# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GetHostStatus', '0003_auto_20181017_1611'),
    ]

    operations = [
        migrations.CreateModel(
            name='historydata',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.CharField(unique=True, max_length=64, verbose_name=b'ip')),
                ('operator', models.CharField(max_length=16, verbose_name=b'operator')),
                ('createtime', models.DateTimeField(verbose_name='\u64cd\u4f5c\u65f6\u95f4')),
                ('type', models.CharField(max_length=32, verbose_name=b'type', choices=[(b'N', '\u7acb\u523b\u68c0\u67e5'), (b'A', '\u52a0\u5165\u81ea\u52a8\u68c0\u67e5')])),
            ],
            options={
                'verbose_name': 'history',
                'verbose_name_plural': 'history',
            },
        ),
        migrations.AlterModelOptions(
            name='ip_list',
            options={'verbose_name': 'iplist', 'verbose_name_plural': 'iplist'},
        ),
    ]
