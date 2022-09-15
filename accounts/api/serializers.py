from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(**attrs)
        if user:
            return user
        raise serializers.ValidationError({'error': 'this user is not exist'})    

    def save(self, validated_data):
        refresh = RefreshToken.for_user(validated_data)
        return ({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
                
