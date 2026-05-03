from rest_framework import serializers
from .models import Class, Section, Timetable

class ClassSerializer(serializers.ModelSerializer):
    subjects = serializers.StringRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Class
        fields = ('id', 'name', 'subjects', 'created_at', 'updated_at')

class SectionSerializer(serializers.ModelSerializer):
    class_name = serializers.CharField(source='class_id.name', read_only=True)
    class_teacher_name = serializers.SerializerMethodField()
    student_count = serializers.IntegerField(source='students.count', read_only=True)

    class Meta:
        model = Section
        fields = ('id', 'name', 'class_id', 'class_name', 'class_teacher', 'class_teacher_name', 'student_count', 'created_at', 'updated_at')

    def get_class_teacher_name(self, obj):
        if obj.class_teacher and obj.class_teacher.user:
            return obj.class_teacher.user.get_full_name() or obj.class_teacher.user.email
        return None

class TimetableSerializer(serializers.ModelSerializer):
    section_name = serializers.CharField(source='section.name', read_only=True)
    class_name = serializers.CharField(source='section.class_id.name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    teacher_name = serializers.SerializerMethodField()

    class Meta:
        model = Timetable
        fields = ('id', 'section', 'section_name', 'class_name', 'day', 'start_time', 'end_time', 'subject', 'subject_name', 'teacher', 'teacher_name', 'created_at', 'updated_at')

    def get_teacher_name(self, obj):
        if obj.teacher and obj.teacher.user:
            return obj.teacher.user.get_full_name() or obj.teacher.user.email
        return None
