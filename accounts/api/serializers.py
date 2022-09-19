from accounts.models import User
from django.contrib.auth import authenticate, password_validation
from rest_framework import serializers
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
                

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email','password','full_name')
        extra_kwargs = {
            'password':{'write_only': True},
        }

    def validate_password(self, value):
        try:
            password_validation.validate_password(value, self.instance)
        except serializers.ValidationError as error:
            self.add_error('password', error)
        return value


class GetOtpSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=4)


    def save(self, validated_data):
        refresh = RefreshToken.for_user(validated_data)
        return ({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })


class UserProfileSerializer(serializers.Serializer):
    email = serializers.EmailField()
    full_name = serializers.CharField()
        