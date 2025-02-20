from django.contrib import admin
from .models import Tool, Category

@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'category', 'is_popular')
    search_fields = ('name',)
    list_filter = ('category', 'is_popular')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)