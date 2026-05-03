from rest_framework import serializers
from .models import Subject

class SubjectSerializer(serializers.ModelSerializer):
    class_names = serializers.StringRelatedField(source='classes', many=True, read_only=True)
    teacher_names = serializers.StringRelatedField(source='teachers', many=True, read_only=True)

    class Meta:
        model = Subject
        fields = ('id', 'name', 'classes', 'class_names', 'teachers', 'teacher_names', 'created_at', 'updated_at')
