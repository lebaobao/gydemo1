# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GetHostStatus', '0002_auto_20181017_1000'),
    ]

    operations = [
        migrations.CreateModel(
            name='ip_list',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.CharField(unique=True, max_length=64, verbose_name=b'ip')),
                ('bizid', models.CharField(max_length=16, verbose_name=b'bizid')),
            ],
        ),
        migrations.AlterField(
            model_name='cpudata',
            name='checkdate',
            field=models.CharField(max_length=128, null=True, verbose_name=b'checkdate', blank=True),
        ),
    ]
