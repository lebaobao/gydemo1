# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CpuData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.CharField(max_length=64, null=True, verbose_name=b'ip', blank=True)),
                ('check_date', models.CharField(max_length=64, verbose_name=b'check_date')),
                ('Mem', models.CharField(max_length=64, verbose_name=b'Mem')),
                ('Disk', models.CharField(max_length=64, verbose_name=b'Disk')),
                ('Cpu', models.CharField(max_length=64, verbose_name=b'Cpu')),
                ('creat_time', models.DateTimeField(verbose_name='\u521b\u5efa\u65f6\u95f4')),
            ],
            options={
                'verbose_name': 'cpu\u5185\u5b58\u78c1\u76d8\u6570\u636e',
                'verbose_name_plural': 'cpu\u5185\u5b58\u78c1\u76d8\u6570\u636e',
            },
        ),
    ]
