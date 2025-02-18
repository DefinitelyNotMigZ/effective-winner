from django.contrib import admin
from .models import Stores, Users

@admin.register(Stores)
class StoresAdmin(admin.ModelAdmin):
    list_display = ('id', 'store_name', 'main_product', 'floor_location', 'user', 'created_at', 'updated_at')
    list_filter = ('user', 'floor_location', 'created_at')
    search_fields = ('store_name', 'main_product', 'user__email', 'user__username')
    readonly_fields = ('id', 'created_at', 'updated_at')
    ordering = ('-created_at',)

@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'created_at')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    readonly_fields = ('id', 'created_at', 'updated_at')
    ordering = ('-created_at',)
