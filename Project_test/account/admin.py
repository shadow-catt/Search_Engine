from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from . import  models
from .models import Account


admin.site.register(Account, UserAdmin)
admin.site.register(models.AdjustInfo)
admin.site.register(models.AdjustJobs)
admin.site.register(models.Administrator)
admin.site.register(models.Collect)
admin.site.register(models.Company)
admin.site.register(models.CompanyAccount)
admin.site.register(models.History)
admin.site.register(models.HistoryRecord)
admin.site.register(models.Job)
admin.site.register(models.OrdinaryAccount)
admin.site.register(models.Recharge)
admin.site.register(models.RechargeInfo)
admin.site.register(models.Requirement)
admin.site.register(models.Search)
admin.site.register(models.ViewInfo)