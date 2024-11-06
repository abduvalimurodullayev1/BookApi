from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework import status, response
from apps.users.serializers import RegisterSerializer, VerificationEmailSerializers, LoginSerializer, \
    ForgotPasswordSerializer, ForgotChangePasswordSerializer, ChangePasswordSerializers
from apps.users.utils import generate_verification_code, send_verification_email, send_forgot_password_email
from apps.users.models import User


class RegisterApiView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=RegisterSerializer,
        responses={
            status.HTTP_201_CREATED: "User successfully registered",
            status.HTTP_400_BAD_REQUEST: "Invalid Credentials"
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            verification_code = generate_verification_code()
            expire_time = timezone.now() + timedelta(minutes=2)
            serializer.save(verification_code=verification_code, activation_key_expires=expire_time)
            send_verification_email(to_email=serializer.validated_data['email'], verification_code=verification_code)
            return Response("Emailga tasdiqlash kodi yuborildi tasdiqlab yuboring", status=status.HTTP_201_CREATED)
        return Response("Xatolik")


class VerifyEmailView(APIView):
    serializer = VerificationEmailSerializers

    @swagger_auto_schema(
        request_body=serializer
    )
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        verification_code = request.data.get("verification_code")
        try:
            instance = User.objects.get(email=email,
                                        verification_code=verification_code)
            if not instance.is_active and instance.activation_key_expires > timezone.now():
                instance.is_active = True
                instance.save()
                return Response({"message": "Email tasdiqlandi"},
                                status=status.HTTP_200_OK)
            elif instance.is_active:
                return Response({"message": "Email allaqachon tadqilangan."},
                                status=status.HTTP_400_BAD_REQUEST)
            elif instance.activation_key_expires < timezone.now() or instance.verification_code != verification_code:
                instance.delete()
                return Response({"message": "Tasdiqlash kodi eskirgan yoki xato "},
                                status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"message": "Noto'g'ri tasdiqlash kod yoki email"}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={
            status.HTTP_200_OK: "Tizimga muafaqqiyatli",
            status.HTTP_400_BAD_REQUEST: "Xato ma'lumotlar"
        }
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data.get("email"))
        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            password = serializer.validated_data.get("password")
            user = authenticate(username=email,
                                password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)
                return Response(data={"message": "Tizimga kirdingiz",
                                      'access token': access_token,
                                      'refresh token': refresh_token},
                                status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordAPIView(APIView):
    @swagger_auto_schema(
        request_body=ForgotPasswordSerializer,
        responses={
            status.HTTP_200_OK: "Success",
            status.HTTP_400_BAD_REQUEST: "Bad Request"
        }
    )
    def post(self, request):
        email = request.data.get("email")
        try:
            user = User.objects.get(email=email)
            verification_code = generate_verification_code()
            expiration_time = timezone.now() + timedelta(minutes=5)
            user.verification_code = verification_code
            user.activation_key_expires = expiration_time
            user.save()

            send_forgot_password_email(to_email=email, verification_code=verification_code)
            return Response({"message": "Parolni tilash uchun emailga xabar yuborildi"},
                            status=status.HTTP_200_OK)
        except User.DoesNotExists:
            return Response({"message": "Foydalanuvchi email manzili topilmadi!!"},
                            status=status.HTTP_404_NOT_FOUND)


class VerifyForgotEmail(APIView):
    @swagger_auto_schema(
        request_body=ForgotChangePasswordSerializer,
        responses={
            status.HTTP_200_OK: "Email tasdiqlandi va parol o'zgardi.",
            status.HTTP_400_BAD_REQUEST: "Tasdiqlash kod muddati tugagan yoki noto'g'ri tasdiqlash kod.",
            status.HTTP_404_NOT_FOUND: "Noto'g'ri tasdiqlash kod yoki email.", }
    )
    def post(self, request):
        email = request.get("email")
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")
        verification_code = request.data.get("verification_code")

        try:
            user = User.objects.get(email=email, verification_code=verification_code)
            if user.activation_key_expires > timezone.now():
                if new_password != confirm_password:
                    return Response({"message": "Parol va tasdiqlash mos kelmadi"},
                                    status=status.HTTP_400_BAD_REQUEST)
                user.set_password(new_password)
                user.is_verified = True
                user.save()
                return Response({'message': "Tasdiqlash kod muddati o'tgan yoki noto'g'ri tasdiqlash kodi"},
                                status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'message': "Noto'g'ri tasdiqlash kod yoki email"}, status=status.HTTP_404_NOT_FOUND)


class ChangePasswordView(APIView):
    @swagger_auto_schema(
        request_body=ChangePasswordSerializers,
        responses={
            status.HTTP_200_OK: "Password o'zgardi",
            status.HTTP_400_BAD_REQUEST: "O'zgarmadi xato urinish",
            status.HTTP_401_UNAUTHORIZED: "Boshqa xato taqiqlangan"
        }
    )
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'message': "Foydalanuvchi autentifikatsiya qilmagan"},
                            status=status.HTTP_401_UNAUTHORIZED)
        serializer = ChangePasswordSerializers(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data['password']
            user = request.user
            if user.is_verified:
                user.set_password(password)
                user.save()
                cache.delete(f'user_{user.id}')
                return Response({'message': "Parol muaffaqiyatli o'zgartirildi"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Foydalanuvchi emaili tasdiqlanmagan"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
