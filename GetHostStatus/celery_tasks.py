# -*- coding: utf-8 -*-

"""
celery 任务

本地启动celery命令: python  manage.py  celery  worker  --settings=settings
周期性任务还需要启动celery调度命令：python  manage.py  celerybeat --settings=settings
"""
import datetime
import time

from celery import task, chain
from celery.schedules import crontab
from celery.task import periodic_task

from common.log import logger

from blueking.component.shortcuts import get_client_by_user

from GetHostStatus.utils import get_job_instance_id, get_host_cpu
from GetHostStatus.models import ip_list

@task()
def async_task(username):
    """
    定义一个 celery 异步任务
    """
    # 执行Job作业，并获取磁盘容量信息写入库

    save_task_log(username)
    logger.error(u"get cpu celery任务执行成功")


@periodic_task(run_every=crontab(minute='*/1', hour='*', day_of_week="*"))
def get_time():
    """
    celery 周期任务示例

    run_every=crontab(minute='*/1', hour='*', day_of_week="*")：每 1 分钟执行一次任务
    periodic_task：程序运行时自动触发周期任务
    """
    save_task_log()
    now = datetime.datetime.now()
    logger.error(u"get cpu celery 周期任务调用成功，当前时间：{}".format(now))

def save_task_log(username='admin'):
    """
    执行 celery 异步任务

    调用celery任务方法:
        task.delay(arg1, arg2, kwarg1='x', kwarg2='y')
        task.apply_async(args=[arg1, arg2], kwargs={'kwarg1': 'x', 'kwarg2': 'y'})
        delay(): 简便方法，类似调用普通函数
        apply_async(): 设置celery的额外执行选项时必须使用该方法，如定时（eta）等
                      详见 ：http://celery.readthedocs.org/en/latest/userguide/calling.html
    """
    iplist=ip_list.objects.all()
    for checkip in iplist:
        biz_id = checkip.bizid              # 你需要执行的业务ID
        ip = checkip.ip        # 您需要执行的业务IP
        alllogs = []
        ## 使用该方式调用云API时，请先将您的SaaS APPID 加入白名单 http://xx.xx.xx.xx/admin/bkcore/functioncontroller/
        client = get_client_by_user(username)
        result, job_instance_id = get_job_instance_id(client, biz_id, ip)
        while True:
            is_finish, capacity_data = get_host_cpu(client, biz_id, job_instance_id, ip)
            if is_finish:
                break
