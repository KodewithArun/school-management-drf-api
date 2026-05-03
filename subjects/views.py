from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Subject
from .serializers import SubjectSerializer
from accounts.permissions import IsPrincipalOrReadOnly

class SubjectListCreateView(APIView):
    permission_classes = [IsPrincipalOrReadOnly]

    def get(self, request):
        subjects = Subject.objects.all()
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = SubjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SubjectDetailView(APIView):
    permission_classes = [IsPrincipalOrReadOnly]

    def get_object(self, pk):
        return get_object_or_404(Subject, pk=pk)

    def get(self, request, pk):
        subject_obj = self.get_object(pk)
        serializer = SubjectSerializer(subject_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        subject_obj = self.get_object(pk)
        serializer = SubjectSerializer(subject_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        subject_obj = self.get_object(pk)
        subject_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
