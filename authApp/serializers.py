from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'phone_number', 'password']
        extra_kwargs = {'username': {'help_text': ''}, }


    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only = True)

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        password = attrs.get('password')

        user = User.objects.filter(email=email).first()

        if not user:
            raise serializers.ValidationError('User not Found!!!')
        
        user = authenticate(username=username, password=password)
        
        if not user:
            raise serializers.ValidationError('Invalid credentials!!')
        
        attrs['user'] = user
        return attrs
    
    
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs
    
    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            pass


    