from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Student
from .serializers import StudentSerializer
from accounts.permissions import IsPrincipalOrReadOnly

class StudentListCreateView(APIView):
    permission_classes = [IsPrincipalOrReadOnly]

    def get(self, request):
        students = Student.objects.all()
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

    def get_object(self, pk):
        return get_object_or_404(Student, pk=pk)

    def get(self, request, pk):
        student_obj = self.get_object(pk)
        serializer = StudentSerializer(student_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        student_obj = self.get_object(pk)
        serializer = StudentSerializer(student_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        student_obj = self.get_object(pk)
        student_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
