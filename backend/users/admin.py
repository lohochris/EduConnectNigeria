from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser  # Ensure CustomUser is imported

class UserAdmin(BaseUserAdmin):
    model = CustomUser
    list_display = ('id', 'email', 'phone_number', 'role', 'date_joined', 'is_active')  # Use fields that exist
    list_filter = ('role', 'is_active')
    search_fields = ('email',)
    ordering = ('-date_joined',)

    readonly_fields = ('date_joined',)  # date_joined is non-editable

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('phone_number', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),  #  
    )

    add_fieldsets = (
        (None, {'fields': ('email', 'password1', 'password2')}),
        ('Personal info', {'fields': ('phone_number', 'role')}),
    )

admin.site.register(CustomUser, UserAdmin)
