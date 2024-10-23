from django.utils.translation import gettext as _
from django.core.mail import send_mail
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
import random
from config import settings
from .models import CustomUser
from .serializers import (
    RegistrationSerializer,
    SendCodeSerializer,
    VerifyCodeSerializer,
    LoginSerializer,
    ResetPasswordSerializer,
    ResetPasswordVerifySerializer,
    ChangePasswordSerializer,
)


# Функция для генерации кода сброса пароля
def generate_reset_code():
    return str(random.randint(1000, 9999))  # Простой 4-значный код


def send_password_reset_code(email):
    reset_code = generate_reset_code()  # Генерация кода сброса пароля
    try:
        user = CustomUser.objects.get(email=email)
        user.reset_code = reset_code
        user.save()

        # Сообщение для отправки по email
        message = (
            f"Здравствуйте, {user.email}!\n\n"
            f"Ваш код для восстановления пароля: {reset_code}\n\n"
            f"С наилучшими пожеланиями,\nКоманда {settings.BASE_URL}"
        )

        send_mail(
            'Восстановление пароля',
            message,  # Передаем сообщение
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

        return Response({
            'response': True,
            'message': _('Письмо с инструкциями по восстановлению пароля было отправлено на ваш email.')
        })

    except CustomUser.DoesNotExist:
        return Response({
            'response': False,
            'message': _('Пользователь с этим адресом электронной почты не найден.')
        }, status=status.HTTP_404_NOT_FOUND)


class RegisterCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegistrationSerializer


class LoginCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(data, status=status.HTTP_200_OK)


class ResetPasswordView(generics.GenericAPIView):
    """Запрос на сброс пароля."""
    serializer_class = ResetPasswordSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        return send_password_reset_code(email)  # Отправка кода сброса пароля


class ResetPasswordVerifyView(generics.GenericAPIView):
    """Подтверждение сброса пароля."""
    serializer_class = ResetPasswordVerifySerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        reset_code = serializer.validated_data['reset_code']

        try:
            user = CustomUser.objects.get(reset_code=reset_code)
            user.reset_code = ''  # Очищаем код сброса после подтверждения
            user.save()

            token, created = Token.objects.get_or_create(user=user)

            return Response({
                'response': True,
                'message': _('Код успешно подтвержден. Теперь можно сменить пароль.'),
                'token': token.key  # Отправляем токен для авторизации
            }, status=status.HTTP_200_OK)

        except CustomUser.DoesNotExist:
            return Response({
                'response': False,
                'message': _('Неверный код для сброса пароля.')
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'response': False,
                'message': _('Произошла ошибка при подтверждении сброса пароля.')
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]  # Только аутентифицированные пользователи могут изменить пароль

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Логика изменения пароля
        user = request.user  # Получите текущего пользователя
        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response({
            'response': True,
            'message': _('Пароль успешно изменен.')
        }, status=status.HTTP_200_OK)


#import random
from django.core.mail import send_mail
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.utils.translation import gettext as _
from config import settings
from .models import CustomUser
from .serializers import (
    RegistrationSerializer,
    SendCodeSerializer,
    VerifyCodeSerializer,
    LoginSerializer,
    ResetPasswordSerializer,
    ResetPasswordVerifySerializer,
    ChangePasswordSerializer,
)


# Функция для генерации кода сброса пароля
def generate_reset_code():
    return str(random.randint(1000, 9999))  # Простой 4-значный код


def send_password_reset_code(email):
    reset_code = generate_reset_code()  # Генерация кода сброса пароля
    try:
        user = CustomUser.objects.get(email=email)
        user.reset_code = reset_code
        user.save()

        # Сообщение для отправки по email
        message = (
            f"Здравствуйте, {user.email}!\n\n"
            f"Ваш код для восстановления пароля: {reset_code}\n\n"
            f"С наилучшими пожеланиями,\nКоманда {settings.BASE_URL}"
        )

        send_mail(
            'Восстановление пароля',
            message,  # Передаем сообщение
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

        return Response({
            'response': True,
            'message': _('Письмо с инструкциями по восстановлению пароля было отправлено на ваш email.')
        })

    except CustomUser.DoesNotExist:
        return Response({
            'response': False,
            'message': _('Пользователь с этим адресом электронной почты не найден.')
        }, status=status.HTTP_404_NOT_FOUND)


class RegisterCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegistrationSerializer


class LoginCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(data, status=status.HTTP_200_OK)


class ResetPasswordView(generics.GenericAPIView):
    """Запрос на сброс пароля."""
    serializer_class = ResetPasswordSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        return send_password_reset_code(email)  # Отправка кода сброса пароля


class ResetPasswordVerifyView(generics.GenericAPIView):
    """Подтверждение сброса пароля."""
    serializer_class = ResetPasswordVerifySerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        reset_code = serializer.validated_data['reset_code']

        try:
            user = CustomUser.objects.get(reset_code=reset_code)
            user.reset_code = ''  # Очищаем код сброса после подтверждения
            user.save()

            token, created = Token.objects.get_or_create(user=user)

            return Response({
                'response': True,
                'message': _('Код успешно подтвержден. Теперь можно сменить пароль.'),
                'token': token.key  # Отправляем токен для авторизации
            }, status=status.HTTP_200_OK)

        except CustomUser.DoesNotExist:
            return Response({
                'response': False,
                'message': _('Неверный код для сброса пароля.')
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'response': False,
                'message': _('Произошла ошибка при подтверждении сброса пароля.')
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [AllowAny]  # Измените на нужную вам permission class

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Логика изменения пароля
        user = request.user  # Получите текущего пользователя
        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response({
            'response': True,
            'message': _('Пароль успешно изменен.')
        }, status=status.HTTP_200_OK)
