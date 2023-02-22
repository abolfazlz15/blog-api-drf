from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from accounts.api import views

app_name = 'accounts'
urlpatterns = [
    # JWT URL
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # login URL
    path('login', views.UserLoginView.as_view(), name='login'),

    # register URL
    path('register', views.UserRegisterView.as_view(), name='register'),
    path('check', views.CheckOtpCodeView.as_view(), name='check-otp'),

    # user profile URL
    path('user', views.UserProfileView.as_view(), name='user-profile'),
    path('user/update', views.UpdateEmailView.as_view(), name='user-edit-profile'),
    path('user/update/check', views.VerifyOTPView.as_view(), name='user-edit-profile-check-email'),

]