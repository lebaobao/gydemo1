# -*- coding: utf-8 -*-

from common.mymako import render_mako_context

from home_application.celery_tasks import async_task
import time
def home(request):
    """
    首页
    """
    async_task.delay(1,2)


    return render_mako_context(request, '/home_application/home.html')


def dev_guide(request):
    """
    开发指引
    """
    return render_mako_context(request, '/home_application/dev_guide.html')


def contactus(request):
    """
    联系我们
    """
    return render_mako_context(request, '/home_application/contact.html')
