# -*- coding: utf-8 -*-

from django.conf.urls import patterns

urlpatterns = patterns(
    'GetHostStatus.views',
    (r'^$', 'home'),
    # 表单下拉数据获取及渲染
    (r'^get_biz_list/$', 'get_biz_list'),
    (r'^get_ip_by_bizid/$', 'get_ip_by_bizid'),
    # 执行作业，获取容量数据
    (r'^get_host/$', 'get_host'),
    (r'^hoststatus/$', 'hoststatus'),
    #增减定时查询任务主机列表
    (r'^add_iplist/$', 'add_iplist'),
    (r'^remove_iplist/$', 'remove_iplist'),
    (r'^get_cpu_chartdata/$','get_cpu_chartdata'),
    (r'^history/$', 'history'),
    (r'^get_historydata/$', 'get_historydata'),






    # 执行作业，获取容量数据

    (r'^execute_job/$', 'execute_job'),
    (r'^get_cpu/$', 'get_cpu'),


   # (r'^hoststatus/$', 'hoststatus'),
    #(r'^history/$', 'history'),


)
