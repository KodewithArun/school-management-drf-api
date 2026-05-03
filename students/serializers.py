from rest_framework import serializers
from .models import Student
from accounts.serializers import UserSerializer

class StudentSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)
    class_names = serializers.StringRelatedField(source='classes', many=True, read_only=True)
    
    class Meta:
        model = Student
        fields = ('id', 'user', 'user_details', 'classes', 'class_names', 'created_at', 'updated_at')
