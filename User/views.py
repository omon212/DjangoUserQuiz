import random, logging, redis
from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import send_mail
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import UserModel
from .serializers import RegisterSerializer, OTPCheckSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings

logger = logging.getLogger(__name__)

r = redis.StrictRedis(
    host='localhost',
    port=6379,
    db=0,
    decode_responses=True
)


class RegisterAPIView(APIView):
    serializer_class = RegisterSerializer

    # @swagger_auto_schema(request_body=serializer_class)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            otp_code = str(random.randint(100000, 999999))

            user = UserModel.objects.create(
                email=email,
                password=make_password(password),
                otp_code=otp_code
            )
            print(otp_code)
            send_mail(
                subject='Your OTP Code',
                message=f'Your OTP code is {otp_code}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False
            )

            return Response({'message': 'Registered successfully. Check your email for OTP.'}, status=201)
        return Response(serializer.errors, status=400)


class OTPCodeCheckAPIView(APIView):
    serializer_class = OTPCheckSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        otp_code = serializer.validated_data['otp_code']
        ip = self.get_client_ip(request)
        attempts_key = f"otp_attempts:{ip}:{email}"
        block_key = f"otp_block:{ip}:{email}"
        if r.exists(block_key):
            ttl = r.ttl(block_key) // 60
            return Response({'error': f'Too many attempts. Try again in {ttl} minutes.'},
                            status=403)
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return Response({'error': 'Invalid email'}, status=400)
        if user.otp_code != otp_code:
            attempts = r.incr(attempts_key)
            r.expire(attempts_key, 3600)

            if attempts >= 3:
                r.set(block_key, "1", ex=3600)
                return Response({'error': 'Too many wrong attempts. Locked for 1 hour.'},
                                status=403)
            return Response({'error': 'Invalid OTP code'}, status=400)
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        r.delete(attempts_key)
        r.delete(block_key)
        user.otp_code = ""
        user.save(update_fields=['otp_code'])
        return Response({
            'refresh': str(refresh),
            'access': str(access)
        }, status=200)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class LoginAPIView(APIView):
    serializer_class = LoginSerializer

    # @swagger_auto_schema(request_body=serializer_class)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)
        if not check_password(password, user.password):
            return Response({'error': 'Invalid password'}, status=400)
        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }, status=200)


class CheckAuthUser(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        print(user)
        logger.debug(f"User object: {user}")
        if user.is_authenticated:
            logger.debug("User is authenticated")
            return Response({'message': 'You are authorized', 'user': str(user)})
        logger.debug("User not authenticated")
        return Response({'detail': 'User not found'}, status=401)
