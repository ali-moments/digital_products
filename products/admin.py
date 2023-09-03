from django.contrib import admin

from import_export.admin import ImportExportModelAdmin

from .models import Product, File, Category

@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['parent', 'title', 'is_enable', 'create_time']
    list_filter = ['is_enable', 'parent']
    search_fields = ['title']

class FileInlineAdmin(admin.StackedInline):
    model = File
    fields = ['title', 'file_type', 'file', 'is_enable']
    extra = 0

@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['title', 'is_enable', 'create_time']
    list_filter = ['is_enable']
    search_fields = ['title']
    filter_horizontal = ['categories']
    inlines = [FileInlineAdmin]
