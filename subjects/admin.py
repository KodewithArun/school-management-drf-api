from django.contrib import admin
from .models import Subject


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at')
    list_filter = ('is_active', 'classes')
    search_fields = ('name',)
    filter_horizontal = ('classes', 'teachers')
    ordering = ('name',)
    readonly_fields = ('created_at', 'updated_at')
