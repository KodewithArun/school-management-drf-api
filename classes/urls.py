from django.urls import path
from .views import (
    ClassListCreateView, ClassDetailView,
    SectionListCreateView, SectionDetailView,
    TimetableListCreateView, TimetableDetailView
)

urlpatterns = [
    path('classes/', ClassListCreateView.as_view(), name='class-list'),
    path('classes/<int:pk>/', ClassDetailView.as_view(), name='class-detail'),
    
    path('sections/', SectionListCreateView.as_view(), name='section-list'),
    path('sections/<int:pk>/', SectionDetailView.as_view(), name='section-detail'),
    
    path('timetables/', TimetableListCreateView.as_view(), name='timetable-list'),
    path('timetables/<int:pk>/', TimetableDetailView.as_view(), name='timetable-detail'),
]
