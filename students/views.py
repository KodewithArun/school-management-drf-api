from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Student
from .serializers import StudentSerializer
from accounts.permissions import IsPrincipalOrReadOnly

class StudentListCreateView(APIView):
    permission_classes = [IsPrincipalOrReadOnly]
    serializer_class = StudentSerializer

    def get(self, request):
        from rest_framework.pagination import PageNumberPagination
        students = Student.objects.select_related('user').prefetch_related('classes').all().order_by('-created_at')
        paginator = PageNumberPagination()
        page = paginator.paginate_queryset(students, request)
        if page is not None:
            serializer = StudentSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentDetailView(APIView):
    permission_classes = [IsPrincipalOrReadOnly]
    serializer_class = StudentSerializer

    def get_object(self, pk):
        return get_object_or_404(Student, pk=pk)

    def get(self, request, pk):
        student = self.get_object(pk)
        serializer = StudentSerializer(student)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        student = self.get_object(pk)
        serializer = StudentSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        student = self.get_object(pk)
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
