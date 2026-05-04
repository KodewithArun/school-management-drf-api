from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Teacher
from .serializers import TeacherSerializer
from accounts.permissions import IsPrincipalOrReadOnly

class TeacherListCreateView(APIView):
    permission_classes = [IsPrincipalOrReadOnly]
    serializer_class = TeacherSerializer

    def get(self, request):
        from rest_framework.pagination import PageNumberPagination
        teachers = Teacher.objects.all()
        paginator = PageNumberPagination()
        page = paginator.paginate_queryset(teachers, request)
        if page is not None:
            serializer = TeacherSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        serializer = TeacherSerializer(teachers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TeacherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TeacherDetailView(APIView):
    permission_classes = [IsPrincipalOrReadOnly]
    serializer_class = TeacherSerializer

    def get_object(self, pk):
        return get_object_or_404(Teacher, pk=pk)

    def get(self, request, pk):
        teacher_obj = self.get_object(pk)
        serializer = TeacherSerializer(teacher_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        teacher_obj = self.get_object(pk)
        serializer = TeacherSerializer(teacher_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        teacher_obj = self.get_object(pk)
        teacher_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
