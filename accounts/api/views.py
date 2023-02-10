from django.core.cache import cache
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.api import serializers
from accounts.models import User
from accounts.otp_service import OTP


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
            cd = serializer.validated_data
            otp_service = OTP()
            otp_service.generate_otp(cd['email'])
            cache.set(key='register', value={
                'email': cd['email'], 'password': cd['password'], 'full_name': cd['full_name']},
                      timeout=300)

            return Response({'email': cd['email'], 'result': 'email sended'}, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


class CheckOtpCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = cache.get(key='register')
        serializer = serializers.GetOtpSerializer(data=request.data)
        otp_obj = OTP()
        if data is None:
            return Response({'error': 'this code not exist or invalid'}, status=status.HTTP_404_NOT_FOUND)
        if serializer.is_valid():
            clean_data = serializer.validated_data
            if otp_obj.verify_otp(otp=clean_data['code'], email=data['email']):
                user = User.objects.create_user(
                    email=data['email'], full_name=data['full_name'], password=data['password'])

                result = serializer.save(validated_data=user)
                return Response(result, status=status.HTTP_201_CREATED)
            return Response({'error': 'this code not exist or invalid'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = serializers.UserProfileSerializer(instance=request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateEmailView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.UserProfileSerializer

    def put(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            full_name = serializer.validated_data.get('full_name')
            user = request.user
            otp_service = OTP()
        
            if email == None:
                email = request.user.email

            if full_name == None:
                full_name = request.user.full_name

            if email != user.email:
                otp = otp_service.generate_otp(email)
                if otp:
                    user.full_name = full_name
                    user.save()
                    otp_service.send_otp(otp, email)
                    cache.set(key='edit_email', value={'email': email, 'code': otp}, timeout=300)
                    return Response({"detail": "OTP sent to the new email address. Provide the OTP for email verification",
                                     "status": status.HTTP_202_ACCEPTED})
                else:
                    return Response(
                        {"detail": "Unable to send OTP, Please try again", "status": status.HTTP_400_BAD_REQUEST})
            else:
                user.email = email
                user.full_name = full_name 
                user.save()

                return Response({'result': 'your profile is updated'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        test = cache.get(key='edit_email')
        code = request.data['code']
        otp_service = OTP()
        is_valid = otp_service.verify_otp(otp=code, email=test['email'])
        if is_valid:
            user = request.user
            user.email = test['email']
            user.save()
            cache.delete(test)
            otp_service.clear_otp(test['email'])
            return Response({'result': 'your profile was updated'}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({"detail": "Invalid OTP or OTP expired", "status": status.HTTP_401_UNAUTHORIZED})
