import random
from django.conf import settings
from django.core.mail import send_mail


def send_verification_email(to_email, verification_code):
    subject = 'Email Tasdiqlash'
    message = f"Xush kelibsiz!\n\nEmail tasdiqlash uchun quyidagi kodni kiriting:" \
              f"\n\n{verification_code}\n\nTashrif buyurganingiz uchun rahmat!"
    from_email = settings.EMAIL_HOST_USER
    send_mail(subject, message, from_email, [to_email])


def send_forgot_password_email(to_email, verification_code):
    subject = 'Parolni tiklash'
    message = f"Parolni tiklash uchun quyidagi kodni kiriting:\n\n{verification_code}\n\nRahmat!"
    from_email = settings.EMAIL_HOST_USER
    send_mail(subject, message, from_email, [to_email])


def generate_verification_code():
    return str(random.randint(100000, 999999))
