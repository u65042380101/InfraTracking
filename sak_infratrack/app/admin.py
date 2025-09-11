from django.contrib import admin
from .models import BranchInfo, InternetLink, HelpdeskRecord

@admin.register(BranchInfo)
class BranchInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'branch_code', 'branch_name', 'province', 'region']
    search_fields = ['branch_code', 'branch_name', 'province', 'region']

@admin.register(InternetLink)
class InternetLinkAdmin(admin.ModelAdmin):
    list_display = ['id', 'branch_name', 'proivider', 'speed', 'start_date']
    search_fields = ['branch_name', 'proivider']

@admin.register(HelpdeskRecord)
class HelpdeskRecordAdmin(admin.ModelAdmin):
    list_display = ['id', 'branch_name', 'device', 'provider', 'problem', 'status', 'date']
    search_fields = ['branch_name', 'device', 'provider', 'problem']

