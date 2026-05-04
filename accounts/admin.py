from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('email',)

    # Fields shown when VIEWING/EDITING an existing user
    fieldsets = UserAdmin.fieldsets + (
        ('School Info', {
            'fields': ('role', 'date_of_birth', 'phone_number', 'address')
        }),
    )

    # Fields shown when CREATING a new user via admin
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('School Info', {
            'fields': ('email', 'role')
        }),
    )

