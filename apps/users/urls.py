from django.urls import path

from apps.common.api_endpoints import *
from apps.common.views import health_check_redis
# from apps.users.serializers import ForgotPasswordSerializer
from apps.users.views import *

app_name = "users"

urlpatterns = [
    path("Register/", RegisterApiView.as_view(), name="register"),
    path("Login/", LoginAPIView.as_view(), name="login"),
    path("verify-email", VerifyEmailView.as_view(), name="verify"),
    path("Forgot-password/", ForgotPasswordAPIView.as_view(), name="forgot-password"),
    path("ChangePassword/", ChangePasswordView.as_view(), name="change_password"),
    path("VerifyFogotEmail/", VerifyForgotEmail.as_view(), name="verify-forgot"),
    path("health-check/redis/", health_check_redis, name="health-check-redis"),
]
