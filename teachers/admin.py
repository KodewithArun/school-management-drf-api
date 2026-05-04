from django.contrib import admin
from .models import Teacher


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'get_email', 'is_active', 'created_at')
    list_filter = ('is_active', 'classes')
    search_fields = ('user__email', 'user__first_name', 'user__last_name')
    filter_horizontal = ('classes',)
    ordering = ('user__email',)
    readonly_fields = ('created_at', 'updated_at')

    @admin.display(description='Full Name')
    def get_full_name(self, obj):
        return obj.user.get_full_name() or obj.user.email

    @admin.display(description='Email')
    def get_email(self, obj):
        return obj.user.email
