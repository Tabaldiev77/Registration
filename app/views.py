import random
from datetime import timedelta

from django.core.mail import send_mail
from django.http import JsonResponse
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from config import settings
from .models import CustomUser, VerificationCode
from .serializers import RegistrationSerializer, SendCodeSerializer, VerifyCodeSerializer, LoginSerializer


class RegisterView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterCreateView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegistrationSerializer


class LoginCreateView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(data, status=status.HTTP_200_OK)


# Подтверждение
@api_view(['POST'])
def send_verification_code(request):
    serializer = SendCodeSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        code = ''.join([str(random.randint(0, 9)) for _ in range(4)])

        # Сохраняем код в базе данных
        VerificationCode.objects.create(email=email, code=code)

        # Отправляем код на email
        send_mail(
            'Ваш код подтверждения',
            f'Ваш код: {code}',
            settings.EMAIL_HOST_USER,  # Используем актуальный email отправителя
            [email],
        )

        return Response({'message': 'Код отправлен на ваш email.'}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Верификация кода
@api_view(['POST'])
def verify_code(request):
    serializer = VerifyCodeSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        input_code = serializer.validated_data['code']

        try:
            # Ищем последний код для указанного email
            verification = VerificationCode.objects.filter(email=email).latest('created_at')

            # Проверяем, что код не истек (например, 10 минут)
            if verification.code == input_code and verification.created_at > timezone.now() - timedelta(minutes=10):
                return Response({'message': 'Код успешно подтвержден!'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Неправильный или истекший код.'}, status=status.HTTP_400_BAD_REQUEST)

        except VerificationCode.DoesNotExist:
            return Response({'error': 'Код не найден.'}, status=status.HTTP_404_NOT_FOUND)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
