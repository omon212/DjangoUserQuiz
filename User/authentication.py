from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from .models import UserModel

class CustomJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            raise exceptions.AuthenticationFailed('Authorization header missing')

        parts = auth_header.split()
        if len(parts) != 2:
            raise exceptions.AuthenticationFailed('Authorization header must contain two space-delimited values')

        prefix, token = parts
        if prefix.lower() != 'bearer':
            raise exceptions.AuthenticationFailed('Authorization header must start with Bearer')

        try:
            payload = UntypedToken(token)
        except (InvalidToken, TokenError) as e:
            raise exceptions.AuthenticationFailed(f'Token invalid: {e}')

        user_id = payload.get('id')
        if not user_id:
            raise exceptions.AuthenticationFailed('Invalid token payload: no user ID')

        try:
            user = UserModel.objects.get(id=user_id)
        except UserModel.DoesNotExist:
            raise exceptions.AuthenticationFailed('User not found')

        return (user, None)