from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Student
from .serializers import StudentSerializer
from accounts.permissions import IsPrincipalOrReadOnly

class StudentViewSet(viewsets.ModelViewSet):
    # 1. OPTIMIZATION: Fix N+1 problem right in the base queryset
    queryset = Student.objects.select_related('user').prefetch_related('classes').all()
    
    # 2. REQUIRED: Define the serializer and permissions
    serializer_class = StudentSerializer
    permission_classes = [IsPrincipalOrReadOnly]
    
    # 3. ADVANCED FEATURES: Enable Filtering, Searching, and Ordering
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    # ?is_active=True&user__role=student
    filterset_fields = ['is_active', 'user__role']
    
    # ?search=Aryan (Searches multiple columns automatically)
    search_fields = ['user__email', 'user__first_name', 'user__last_name', 'user__phone_number']
    
    # ?ordering=-created_at
    ordering_fields = ['created_at', 'user__first_name']
