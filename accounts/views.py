from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema
from .serializers import CustomTokenSerializer, UserSerializer, UserRegistrationSerializer
from .permissions import IsPrincipal

class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer

class UserRegistrationView(APIView):
    permission_classes = [IsAuthenticated, IsPrincipal]
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Welcome! Your account has been created successfully. You can now log in."
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PrincipalOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsPrincipal]

    def get(self, request):
        return Response({"message": "Hello Principal!"})

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=LogoutSerializer,
        responses={205: None},
        description="Logout a user by blacklisting their refresh token. Requires Authorization header."
    )
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({
                    "error": "The 'refresh' token is required in the request body."
                }, status=status.HTTP_400_BAD_REQUEST)
                
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({
                "message": "You have been logged out successfully. Have a great day!"
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "error": "Oops! We couldn't log you out. The token might be invalid or already used.",
                "developer_detail": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
