from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import RegisterSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.generics import CreateAPIView

# Create your views here.

class RegisterView(APIView):

    serializer_class = RegisterSerializer
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # <-- key change here
        serializer.save()
        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)

    
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        
class ThrottledTokenObtainPairView(TokenObtainPairView):
    
    throttle_classes = [UserRateThrottle, AnonRateThrottle]