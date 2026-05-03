from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Class, Section, Timetable
from .serializers import ClassSerializer, SectionSerializer, TimetableSerializer
from accounts.permissions import IsPrincipalOrReadOnly, IsTeacherOrReadOnly

class ClassListCreateView(APIView):
    permission_classes = [IsPrincipalOrReadOnly]

    def get(self, request):
        classes = Class.objects.all()
        serializer = ClassSerializer(classes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ClassSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClassDetailView(APIView):
    permission_classes = [IsPrincipalOrReadOnly]

    def get_object(self, pk):
        return get_object_or_404(Class, pk=pk)

    def get(self, request, pk):
        class_obj = self.get_object(pk)
        serializer = ClassSerializer(class_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        class_obj = self.get_object(pk)
        serializer = ClassSerializer(class_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        class_obj = self.get_object(pk)
        class_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class SectionListCreateView(APIView):
    permission_classes = [IsPrincipalOrReadOnly]

    def get(self, request):
        sections = Section.objects.all()
        serializer = SectionSerializer(sections, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = SectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SectionDetailView(APIView):
    permission_classes = [IsPrincipalOrReadOnly]

    def get_object(self, pk):
        return get_object_or_404(Section, pk=pk)

    def get(self, request, pk):
        section_obj = self.get_object(pk)
        serializer = SectionSerializer(section_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        section_obj = self.get_object(pk)
        serializer = SectionSerializer(section_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        section_obj = self.get_object(pk)
        section_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TimetableListCreateView(APIView):
    permission_classes = [IsTeacherOrReadOnly]

    def get(self, request):
        timetables = Timetable.objects.all()
        serializer = TimetableSerializer(timetables, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TimetableSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TimetableDetailView(APIView):
    permission_classes = [IsTeacherOrReadOnly]

    def get_object(self, pk):
        return get_object_or_404(Timetable, pk=pk)

    def get(self, request, pk):
        timetable_obj = self.get_object(pk)
        serializer = TimetableSerializer(timetable_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        timetable_obj = self.get_object(pk)
        serializer = TimetableSerializer(timetable_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        timetable_obj = self.get_object(pk)
        timetable_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
