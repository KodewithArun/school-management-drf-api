from django.contrib import admin
from .models import Class, Section, Timetable


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name',)
    ordering = ('name',)
    readonly_fields = ('created_at', 'updated_at')


class TimetableInline(admin.TabularInline):
    """Shows the timetable slots directly inside the Section detail page."""
    model = Timetable
    extra = 0
    fields = ('day', 'start_time', 'end_time', 'subject', 'teacher')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'class_id', 'class_teacher', 'is_active')
    list_filter = ('class_id', 'is_active')
    search_fields = ('name', 'class_id__name')
    autocomplete_fields = ('class_teacher',)
    filter_horizontal = ('students',)
    inlines = [TimetableInline]
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = ('section', 'day', 'start_time', 'end_time', 'subject', 'teacher')
    list_filter = ('day', 'section__class_id')
    search_fields = ('section__name', 'subject__name', 'teacher__user__email')
    ordering = ('section', 'day', 'start_time')
    readonly_fields = ('created_at', 'updated_at')
