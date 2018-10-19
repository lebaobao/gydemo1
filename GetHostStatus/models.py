# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
import pdb
from datetime import datetime
from django.db import models
from common.log import logger
class CpuDataManager(models.Manager):
    def save_data(self, data):
        """
        保存执行结果数据
        """
        try:
            CpuData.objects.create(
                ip=data['ip'],
                checkdate=data['checkdate'],
                Mem=data['Mem'],
                Disk=data['Disk'],
                Cpu = data['Cpu'],
                creattime=datetime.now(),
            )

            result = {'result': True, 'message': u"保存成功"}
        except Exception, e:
            logger.error(u"save_data %s" % e)
            result = {'result': False, 'message': u"保存失败, %s" % e}
        return result



class CpuData(models.Model):
    """
    存储查询的容量数据
    """
    ip = models.CharField('ip', max_length=64, blank=True, null=True)
    checkdate =  models.CharField('checkdate', max_length=128, blank=True, null=True)
    Mem = models.CharField('Mem', max_length=64)
    Disk = models.CharField('Disk', max_length=64)
    Cpu = models.CharField('Cpu', max_length=64)
    creattime=models.DateTimeField(u'创建时间')
    objects = CpuDataManager()

    def __unicode__(self):
        return self.ip

    class Meta:
        verbose_name = u"cpu内存磁盘数据"
        verbose_name_plural = u"cpu内存磁盘数据"




class ip_listManager(models.Manager):
    def save_data(self, data):
        """
        保存执行结果数据
        """
        try:
            ip_list.objects.create(
                ip=data['ip'],
                bizid=data['bizid'],

            )

            result = {'result': True, 'message': u"保存成功"}
        except Exception, e:
            logger.error(u"save_data %s" % e)
            result = {'result': False, 'message': u"保存失败, %s" % e}
        return result

class ip_list(models.Model):
    #需定时查询的主机IP列表
    ip = models.CharField('ip', max_length=64, unique=True)
    bizid=models.CharField('bizid', max_length=16)
    objects = ip_listManager()

    def __unicode__(self):
        return self.ip

    class Meta:
        verbose_name = u"iplist"
        verbose_name_plural = u"iplist"




class historydataManager(models.Manager):
    def save_data(self, data):
        """
        保存执行结果数据
        """
        try:
            historydata.objects.create(
                ip=data['ip'],
                operator=data['operator'],
                createtime=datetime.now(),
                type=data['type'],
            )

            result = {'result': True, 'message': u"保存成功"}
        except Exception, e:
            logger.error(u"save_data %s" % e)
            result = {'result': False, 'message': u"保存失败, %s" % e}
        return result

class historydata(models.Model):
    ip = models.CharField('ip', max_length=64)
    operator =models.CharField('operator', max_length=16)
    createtime=models.DateTimeField(u'操作时间')
    type=models.CharField('type',max_length=32,choices=(('N',u'立刻检查'),('A',u'加入自动检查'),('D',u'移除自动检查')))
    objects = historydataManager()

    def __unicode__(self):
        return self.id

    class Meta:
        verbose_name = u"historydata"
        verbose_name_plural = u"historydata"