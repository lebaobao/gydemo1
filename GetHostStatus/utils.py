# -*- coding: utf-8 -*-
# 该示例中使用云API V1版本

from common.log import logger
from blueking.component.shortcuts import get_client_by_user
from GetHostStatus.models import CpuData,historydata
import base64
from datetime import datetime
import pdb

def get_job_instance_id(client, biz_id, ip):
    """
    执行Job作业
    """
    # 获取作业模板参数详情
    shell = (
        '#!/bin/bash\n'
        '\n'
        'MEMORY=$(free -m | awk \'NR==2{printf "%.2f%%", $3*100/$2 }\')\n'
        'DISK=$(df -h | awk \'$NF=="/"{printf "%s", $5}\')\n'
        'CPU=$(top -bn1 | grep load | awk \'{printf "%.2f%%", $(NF-2)}\')\n'
        'DATE=$(date "+%Y-%m-%d %H:%M:%S")\n'
        'echo -e "$DATE|$MEMORY|$DISK|$CPU"\n')
    cmd = base64.b64encode(shell)
    kwargs = {
        "bk_biz_id": biz_id,
        "script_id": 4,
        "script_content": cmd,
        "script_timeout": 1000,
        "account": "root",
        "is_param_sensitive": 0,
        "script_type": 1,
        "ip_list": [
            {
                "bk_cloud_id": 0,
                "ip": ip,
            },
        ],
    }
    resp = client.job.fast_execute_script(**kwargs)



    if resp.get('result'):
        job_instance_id = resp.get('data').get('job_instance_id')
    else:
        job_instance_id = -1
    
    return resp.get('result'), job_instance_id


def get_host_cpu(client, biz_id,job_instance_id,ip):
    """
    获取cpn,mem,desk使用信息
    """
    kwargs = {
        'bk_biz_id': biz_id,
        'job_instance_id': job_instance_id,
    }
    resp = client.job.get_job_instance_log(**kwargs)
    is_finish = False


    cpumemdata= {}
    cpumem = " "
    if resp.get('result'):
        #pdb.set_trace()
        data = resp.get('data')
        logs = ''
        _d=data[0]
        if _d.get('is_finished'):
            is_finish = True
            logs = _d['step_results'][0].get('ip_logs')[0].get('log_content')
            cpumem = logs
            logs = logs.split('|')
            if logs and len(logs) >= 3:
                cpu_data={
                    'ip': ip,
                    'checkdate': logs[0],
                    'Mem': logs[1],
                    'Disk': logs[2],
                    'Cpu': logs[3],

                }
                print cpu_data
                #pdb.set_trace()
                res=CpuData.objects.save_data(cpu_data)


                print res

                #回传网页
                date = datetime.now()
                date=date.strftime("%Y-%m-%d %H:%M:%S")
                cpumemdata={
                    "cpumem":cpumem,
                    'date':date,
                }
    return is_finish, cpumemdata
        