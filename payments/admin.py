from django.contrib import admin

from .models import Gateway, Payment

@admin.register(Gateway)
class GatewayAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'is_enable']

    
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'package', 'gateway', 'price', 'status', 'phone_number', 'created_time', 'updated_time']
    list_filter = ['status', 'gateway', 'package']
    search_fields = ['user__username', 'phone_number']
    
