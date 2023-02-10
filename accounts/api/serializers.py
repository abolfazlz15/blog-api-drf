from accounts.models import User
from django.contrib.auth import authenticate, password_validation
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    password = serializers.CharField(required=False)

    def validate(self, attrs):
        user = authenticate(**attrs)

        if user:
            return user
        raise serializers.ValidationError({'error': 'this user is not exist', 'success': False})

    def save(self, validated_data):
        refresh = RefreshToken.for_user(validated_data)
        return ({
            'success': True,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            # 'test': str(refresh.exp),
        })


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'full_name')
        extra_kwargs = {
            'password': {'write_only': True},
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


class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)
    full_name = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ('email', 'full_name')

    def validate_email(self, value):
        user = User.objects.filter(email=value)
        if user:
            raise serializers.ValidationError({'error': 'this email exist'})
        else:
            return value


class GetOtpEmailChangeSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=4)
