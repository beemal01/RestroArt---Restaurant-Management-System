from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import User
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers


# Create your views here.

def signup(request):
    return render(request, 'signup.html')

def signin(request):
    return render(request, 'signin.html')

def cart(request):
    return render(request, 'cart.html')


class signupview(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        serializer.save()


class signinview(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = LoginSerializer

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def post(self, request):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        user_data = RegisterSerializer(user)

        return Response({
            'User' : user_data.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_202_ACCEPTED)
    
  
class logoutview(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
            return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
        except TokenError:
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)
