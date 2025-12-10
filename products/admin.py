from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'vendor', 'price', 'stock', 'status','created_at')
    list_filter = ('vendor', 'status')
    search_fields = ('name', 'description')
    list_editable = ('price', 'stock', 'status',)


