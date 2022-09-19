from random import randint

from accounts.api import serializers
from accounts.models import OTPCode, User
from django.core.cache import cache
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class UserLoginView(APIView):
    def post(self, request):
        serializer = serializers.LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.save(validated_data=serializer.validated_data)
        return Response(result)
 

class UserRegisterView(APIView):
    def post(self, request):
        serializer = serializers.UserRegisterSerializer(data=request.data)

        if serializer.is_valid():
            randcode = randint(1000, 9999)
            cd = serializer.validated_data
            cache.set(key='register', value={'email': cd['email'], 'password': cd['password'], 'full_name': cd['full_name'], 'code': randcode}, timeout=300)
            print(cache.get(key='register'))
            OTPCode.objects.create(code=randcode, email=cd['email'], password=cd['password'])

            mail_subject = 'فعال سازی اکانت'
            message = render_to_string('accounts/active_email.html', {
                'user': cd['email'],
                'code': randcode,
            })
            to_email = cd['email']
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return Response({'email': cd['email'], 'result': 'email sended'})
        return Response(serializer.errors)


class CheckOtpCodeView(APIView):
    def post(self, request):
        data = cache.get(key='register')
        serializer = serializers.GetOtpSerializer(data=request.data)
        otp = OTPCode.objects.get(code=data['code'], email=data['email'])

        expiration_date = otp.expiration_date + timezone.timedelta(minutes=2)
        if expiration_date < timezone.now():
            otp.delete()
            return Response({'error': 'your code is expire'})

        if serializer.is_valid():
            if OTPCode.objects.filter(code=data['code'], email=data['email']).exists():
                user = User.objects.create_user(email=data['email'], full_name=data['full_name'], password=data['password'])

                result = serializer.save(validated_data=user)
                otp.delete()
                return Response(result)
            return Response({'error': 'this code not exist'})    
        return Response(serializer.errors) 


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    
    def get(self, request):
        serializer = serializers.UserProfileSerializer(instance=request.user)
        return Response(serializer.data)
