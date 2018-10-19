# -*- coding: utf-8 -*-
import pdb

from django.shortcuts import render

from GetHostStatus.utils import get_job_instance_id, get_host_cpu
from blueking.component.shortcuts import get_client_by_request
from GetHostStatus.models import CpuData,CpuDataManager,ip_list,historydata

# Create your views here.
from common.mymako import render_mako_context, render_json


def home(request):
    """
    Home Page
    """
    # 执行异步任务查询磁盘数据入库
    # async_task.delay(request.user.username)

    # 执行定时任务查询磁盘数据入库
    # now = datetime.datetime.now()
    # async_task.apply_async(args=[request.user.username], eta=now + datetime.timedelta(seconds=5))

    # 串行任务执行
    # celery_chain_task(
    #     {
    #         'custom_func1': {'param1': 1},
    #         'custom_func2': {'param2': 2},
    #         'custom_func3': {'param3': 3}
    #     }
    # )
    return render_mako_context(request, '/GetHostStatus/home.html')


# ------------------------------------
# 执行参数表单数据获取，业务、ip、作业
# ------------------------------------
def get_biz_list(request):
    """
    获取所有业务
    """
    biz_list = []
    client = get_client_by_request(request)
    kwargs = {
        'fields': ['bk_biz_id', 'bk_biz_name']
    }
    resp = client.cc.search_business(**kwargs)
    if resp.get('result'):
        data = resp.get('data', {}).get('info', {})
        for _d in data:
            biz_list.append({
                'name': _d.get('bk_biz_name'),
                'id': _d.get('bk_biz_id'),
            })

    result = {'result': resp.get('result'), 'data': biz_list}
    return render_json(result)


def get_ip_by_bizid(request):
    """
    获取业务下IP
    """
    biz_id = int(request.GET.get('biz_id'))
    client = get_client_by_request(request)
    kwargs = {'bk_biz_id': biz_id,
              'condition': [
                  {
                      'bk_obj_id': 'biz',
                      'fields': ['bk_biz_id'],
                      'condition': [
                          {
                              'field': 'bk_biz_id',
                              'operator': '$eq',
                              'value': biz_id
                          }
                      ]
                  }
              ]
              }
    resp = client.cc.search_host(**kwargs)
    ip_list = []
    if resp.get('result'):
        data = resp.get('data', {}).get('info', {})
        for _d in data:
            _hostinfo = _d.get('host', {})
            if _hostinfo.get('bk_host_innerip') not in ip_list:
                ip_list.append(_hostinfo.get('bk_host_innerip'))

    ip_all = [{'ip': _ip} for _ip in ip_list]
    result = {'result': resp.get('result'), 'data': ip_all}
    return render_json(result)


def get_host(request):
    """
    获取host信息
    """
    biz_id = int(request.POST.get('biz_id'))

    client = get_client_by_request(request)
    kwargs = {
        "page": {"start": 0, "limit": 5, "sort": "bk_host_id"},
        "ip": {
            "flag": "bk_host_innerip|bk_host_outerip",
            "exact": 1,
            "data": []
        },
        "condition": [
            {
                "bk_obj_id": "host",
                "fields": [],
                "condition": []
            },
            {"bk_obj_id": "module", "fields": [], "condition": []},
            {"bk_obj_id": "set", "fields": [], "condition": []},
            {
                "bk_obj_id": "biz",
                "fields": [
                    "default",
                    "bk_biz_id",
                    "bk_biz_name",
                ],
                "condition": [
                    {
                        "field": "bk_biz_id",
                        "operator": "$eq",
                        "value": biz_id
                    }
                ]
            }
        ]
    }
    resp = client.cc.search_host(**kwargs)
    host_info = []
    if resp.get('result'):
        data = resp.get('data', {}).get('info', {})
        for _d in data:
            _hostinfo = _d.get('host', {})
            _setinfo = _d.get('set', {})
            _moduleinfo = _d.get('module', {})

            if _hostinfo.get('bk_host_innerip') not in host_info:
                item = {
                    "host_id": _hostinfo.get('bk_host_id'),
                    "host_innerip": _hostinfo.get('bk_host_innerip'),
                    "cpu": "",
                    "date": "",
                    "setname": _setinfo[0].get('bk_set_name'),
                    "region": _hostinfo.get('bk_cloud_id')[0].get('bk_inst_name'),
                    "osname": _hostinfo.get('bk_os_type'),
                    "modulename": _moduleinfo[0].get('bk_module_name'),
                }
                host_info.append(item)

    host_all = [{'host': _host} for _host in host_info]
    result = {'result': resp.get('result'), 'data': host_info}

    return render_json(result)


# ------------------------------------
# 执行作业，获取内存、磁盘、cpu数据
# ------------------------------------
def execute_job(request):
    """
    执行磁盘容量查询作业
    """
    biz_id = request.POST.get('biz_id')
    ip = request.POST.get('ip')
    #存储操作记录
    operator = request.user.username
    orderdata = {"ip": ip, "type": 'N', 'operator': operator}


    historydata.objects.save_data(orderdata)


    # 调用作业平台API，或者作业执行实例ID
    client = get_client_by_request(request)
    result, job_instance_id = get_job_instance_id(client, biz_id, ip)

    result = {'result': result, 'data': job_instance_id}
    return render_json(result)


def get_cpu(request):
    """
    获取作业执行结果，并解析执行结果展示
    """
    job_instance_id = request.GET.get('job_instance_id')
    biz_id = request.GET.get('biz_id')
    ip = request.GET.get('ip')

    # 调用作业平台API，或者作业执行详情，解析获取磁盘容量信息
    client = get_client_by_request(request)
    is_finish, cpu_datanew = get_host_cpu(client, biz_id, job_instance_id, ip)
    #pdb.set_trace()



    return render_json({'code': 0, 'message': 'success', 'data': cpu_datanew})








# ------------------------------------
# 添加定时IP
# ------------------------------------
def add_iplist(request):
    """
    添加定时ip列表
    """
    bizid = request.POST.get('biz_id')
    ip = request.POST.get('ip')
    operator=request.user.username
    #增加操作记录
    orderdata={"ip":ip,"type":'A','operator':operator}
    res1=historydata.objects.save_data(orderdata)
    print 'ddddd',res1

    # 调用作业平台API，或者作业执行实例ID
    data={"ip":ip,"bizid":bizid}
    ip_list.objects.save_data(data)



    massage = "添加定时任务成功"
    return render_json({ 'massage': massage,'ip':ip,'result':True})


# ------------------------------------
# 添加定时IP
# ------------------------------------
def remove_iplist(request):
    """
    移除定时ip列表
    """
    bizid = request.POST.get('biz_id')
    ip = request.POST.get('ip')
    operator=request.user.username
    #增加操作记录

    orderdata={"ip":ip,"type":'D','operator':operator}
    res1=historydata.objects.save_data(orderdata)
    print 'ddddd',res1

    #移除定时任务主机
    removedata=ip_list.objects.filter(ip=ip)
    if removedata:
        removedata.delete()



    massage = "移除定时任务成功"
    return render_json({ 'massage': massage,'ip':ip,'result':True})



def hoststatus(request):
    """
    监控图表
    """


    return render_mako_context(request, '/GetHostStatus/hoststatus.html')


def history(request):
    """
    查询历史
    """

    return render_mako_context(request, '/GetHostStatus/history.html/')

def get_historydata(request):
    historydatas=historydata.objects.all()
    hisdatas=[]
    for hisdata in historydatas:

        data={
            'id':hisdata.id,
            'ip':hisdata.ip,
            'operstor':hisdata.operator,
            'createtime':hisdata.createtime.strftime('%Y-%m-%d %H:%M:%S'),
            'type':hisdata.get_type_display()


        }
        hisdatas.append(data)
    result = {'result': True, 'data': hisdatas}

    return render_json(result)

#------------------------------------
# 获取视图数据
#------------------------------------
def get_cpu_chartdata(requset):
    """
    获取视图数据，ip为1.1.1.1
    """

    ip = requset.GET.get('ip')
    cpudatas = CpuData.objects.filter(ip=ip)

    times = []
    data_cpu = []
    data_mem = []
    data_disk = []
    for cpudata in cpudatas:
        times.append(cpudata.creattime.strftime('%Y-%m-%d %H:%M:%S'))
        data_cpu.append(cpudata.Cpu.strip('%\n'))
        data_mem.append(cpudata.Mem.strip('%'))
        data_disk.append(cpudata.Disk.strip('%'))

    result = {
            'code': 0,
            'result': True,
            'messge': 'success',
            'data': {
                'xAxis': times,
                'series' : [
                    {
                        'name': 'cpu' ,
                        'type': 'line',
                        'data': data_cpu
                    },
                    {
                        'name': 'mem' ,
                        'type': 'line',
                        'data': data_mem
                    },
                    {
                        'name': 'disk',
                        'type': 'line',
                        'data': data_disk
                    }

                ]
            }
        }
    return render_json(result)