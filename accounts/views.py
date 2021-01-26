from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Profile
from .permissions import IsAdminUser
from .serializers import ProfileSerializer, ProfileMailSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated & IsAdminUser]
    pagination_class = PageNumberPagination

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=[IsAuthenticated, ])
    def me(self, request):
        user = request.user
        if self.request.method == 'PATCH':
            serializer = self.get_serializer(instance=user, data=request.data,
                                             partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(role=user.role, username=user.username,
                            email=user.email)
        return Response(self.get_serializer(user).data)


class GetConfirmationCode(APIView):
    def post(self, request):
        serializer = ProfileMailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, created = Profile.objects.get_or_create(
            username=serializer.data.get('username'),
            email=serializer.data.get('email')
        )
        confirmation_code = default_token_generator.make_token(user)
        mail.send_mail(
            'Код подтверждения сайта yamdb',
            confirmation_code,
            user.email,
            [settings.SENDER_EMAIL],
        )

        return Response(status=status.HTTP_200_OK)


class GetTokenCode(APIView):
    def post(self, request):
        serializer = ProfileMailSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data=serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(Profile,
                                 email=serializer.data.get('email'),
                                 username=serializer.data.get('username'))
        confirmation_code = serializer.data.get('confirmation_code', None)
        if default_token_generator.check_token(user, confirmation_code):
            refresh = RefreshToken.for_user(user)
            resp = {'refresh': str(refresh),
                    'access': str(refresh.access_token)
                    }
            return Response(data=resp, status=status.HTTP_200_OK)
        return Response(data='Неверный код поддверждения',
                        status=status.HTTP_400_BAD_REQUEST)
