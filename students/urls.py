from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet

# 1. Instantiate the Router
router = DefaultRouter()

router.register(r'', StudentViewSet, basename='student')

# 3. Include the generated URLs
urlpatterns = [
    path('', include(router.urls)),
]
