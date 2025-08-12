from django.urls import path
from .views import *

urlpatterns = [
    path('user/register/', RegisterAPIView.as_view(), name='register'),
    path('user/otp-check/', OTPCodeCheckAPIView.as_view(), name='otp_check'),
    path('user/login/', LoginAPIView.as_view(), name='login'),
    path('user/auth_check/', CheckAuthUser.as_view(), name='auth_check'),
]
