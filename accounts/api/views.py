from django.shortcuts import render
from rest_framework.views import APIView
from accounts.api.serializers import LoginSerializer
from rest_framework.response import Response

class UserLoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.save(validated_data=serializer.validated_data)
        return Response(result)