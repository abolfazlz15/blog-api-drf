from random import randint

from accounts.api import serializers
from accounts.models import OTPCode, User
from django.core.cache import cache
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class UserLoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = serializers.LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.save(validated_data=serializer.validated_data)
        return Response(result, status=status.HTTP_200_OK)
 

class UserRegisterView(APIView):
    permission_classes = [AllowAny]
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
            return Response({'email': cd['email'], 'result': 'email sended'}, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


class CheckOtpCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = cache.get(key='register')
        serializer = serializers.GetOtpSerializer(data=request.data)
        otp = OTPCode.objects.get(code=data['code'], email=data['email'])

        expiration_date = otp.expiration_date + timezone.timedelta(minutes=2)
        if expiration_date < timezone.now():
            otp.delete()
            return Response({'error': 'your code is expire'}, status=status.HTTP_406_NOT_ACCEPTABLE)

        if serializer.is_valid():
            if OTPCode.objects.filter(code=data['code'], email=data['email']).exists():
                user = User.objects.create_user(email=data['email'], full_name=data['full_name'], password=data['password'])

                result = serializer.save(validated_data=user)
                otp.delete()
                return Response(result, status=status.HTTP_201_CREATED)
            return Response({'error': 'this code not exist'}, status=status.HTTP_404_NOT_FOUND)    
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE) 


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]


    def get(self, request):
        serializer = serializers.UserProfileSerializer(instance=request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserEditProfileView(APIView):
    def put(self, request):
        old_email = request.user.email

        instance = User.objects.get(email=request.user.email, full_name=request.user.full_name)
        serializer = serializers.UserProfileSerializer(instance=instance, data=request.data, partial=True)

        if serializer.is_valid():
            data = serializer.validated_data
            serializer.save()

            if old_email != data['email']:
                randcode = randint(1000, 9999)
                OTPCode.objects.create(email=data['email'], code=randcode)
                
                cache.set(key='edit_email', value={'email': data['email'], 'code': randcode}, timeout=300)
                print(cache.get(key='edit_email'))

                # mail_subject = 'فعال سازی اکانت'
                # message = render_to_string('accounts/active_email.html', {
                #     'user': instance.email,
                #     'code': randcode,
                # })
                # to_email = data['email']
                # email = EmailMessage(
                #     mail_subject, message, to=[to_email]
                # )
                # email.send()
                return Response({'result': 'code sended to your email'})
            return Response({'Response': 'updated'})
        return Response(serializer.errors)



class CheckOTPCodeEmailChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = cache.get(key='edit_email')
        serializer = serializers.GetOtpEmailChangeSerializer(data=request.data)
        otp = OTPCode.objects.get(code=data['code'], email=data['email'])
        


        if serializer.is_valid():
            expiration_date = otp.expiration_date + timezone.timedelta(minutes=2)
            if expiration_date < timezone.now():
                otp.delete()
                return Response({'error': 'your code is expire'})

            elif OTPCode.objects.filter(code=data['code'], email=data['email']).exists():
                user = User.objects.get(email=request.user.email)
                user.email = data['email']
                user.save()
                otp.delete()
                return Response({'result': 'your profile was updated'})
            return Response({'error': 'this code not exist'})    
        return Response(serializer.errors)

