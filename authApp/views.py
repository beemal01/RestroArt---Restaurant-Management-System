from django.shortcuts import render
from django.http import HttpResponseRedirect
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import User
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken


# Create your views here.


def redirect_to_canonical_origin(request):
    host = request.get_host().split(':')[0]
    if host != '127.0.0.1':
        return None

    canonical_url = f"{request.scheme}://localhost:8000{request.path}"
    if request.META.get('QUERY_STRING'):
        canonical_url = f"{canonical_url}?{request.META['QUERY_STRING']}"

    return HttpResponseRedirect(canonical_url)

def signup(request):
    redirect_response = redirect_to_canonical_origin(request)
    if redirect_response:
        return redirect_response

    return render(request, 'signup.html')

def signin(request):
    redirect_response = redirect_to_canonical_origin(request)
    if redirect_response:
        return redirect_response

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
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)



