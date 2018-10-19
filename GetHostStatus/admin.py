from django.contrib import admin
from GetHostStatus.models import CpuData,CpuDataManager,ip_list,historydata

# Register your models here.

admin.site.register(CpuData)
admin.site.register(ip_list)
admin.site.register(historydata)
