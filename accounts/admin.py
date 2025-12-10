from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('user_type', 'phone', 'location')}),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {'fields': ('user_type', 'phone', 'location')}),
    )

    list_display = BaseUserAdmin.list_display + ('user_type', 'phone')
    list_filter = BaseUserAdmin.list_filter + ('user_type',)
