from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db import transaction
from .models import Teacher
from accounts.serializers import UserSerializer, UserRegistrationSerializer

User = get_user_model()

class TeacherSerializer(serializers.ModelSerializer):
    # Nested user data for creation
    user_data = UserRegistrationSerializer(write_only=True)
    
    # Nested user details for response
    user_details = UserSerializer(source='user', read_only=True)
    class_names = serializers.StringRelatedField(source='classes', many=True, read_only=True)

    class Meta:
        model = Teacher
        fields = ('id', 'user_data', 'user_details', 'classes', 'class_names', 'created_at', 'updated_at')

    def create(self, validated_data):
        user_data = validated_data.pop('user_data')
        classes = validated_data.pop('classes', [])

        with transaction.atomic():
            # 1. Create User
            user = User.objects.create_user(**user_data)
            user.role = 'teacher'
            user.save()

            # 2. Create Teacher profile
            teacher = Teacher.objects.create(user=user, **validated_data)

            # 3. Handle ManyToMany relationships
            if classes:
                teacher.classes.set(classes)

        return teacher
