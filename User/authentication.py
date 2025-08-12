from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from rest_framework_simplejwt.tokens import AccessToken, TokenError
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework_simplejwt.settings import api_settings
from django.conf import settings
from .models import UserModel

class CustomJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            raise exceptions.AuthenticationFailed('Authorization header must be: Bearer <token>')

        token = parts[1]

        # 1) Avvalo token to'g'riligi (imzo, expiry)ni tekshirish:
        try:
            # AccessToken bilan tekshir: agar refresh yuborilgan bo'lsa bu blok xato beradi
            access = AccessToken(token)
        except TokenError as e:
            raise exceptions.AuthenticationFailed(f'Token invalid: {e}')

        # 2) Token payloadni olish va user_id ni aniqlash:
        # xavfsizlik va moslashuvchanlik uchun API settingdagi claimni olamiz
        user_id_claim = api_settings.USER_ID_CLAIM  # odatda 'user_id'
        user_id = access.get(user_id_claim) or access.get('user_id') or access.get('id')
        if not user_id:
            raise exceptions.AuthenticationFailed('Token payload does not contain user id')

        # 3) DB dan userni topish
        try:
            user = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            raise exceptions.AuthenticationFailed('User not found')

        return (user, None)