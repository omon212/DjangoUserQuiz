from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('otp-check/', OTPCodeCheckAPIView.as_view(), name='otp_check'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('auth_check/', CheckAuthUser.as_view(), name='auth_check'),
]
