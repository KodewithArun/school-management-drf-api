from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenSerializer

class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer