from django.contrib import admin

from import_export.admin import ImportExportModelAdmin

from .models import Package, Subscription

@admin.register(Package)
class PackageAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'title', 'sku', 'is_enable', 'price', 'duration']
    filter_horizontal = ['gateways']


@admin.register(Subscription)
class SubscriptionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'user', 'package', 'created_time', 'expire_time']
