from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

from .serializers import CreateUserSerializer, ReferredUserSerializer, UserSerializer
from .decorators import handle_exceptions
from custom_auth.models import CustomUser


class UserViewSet(GenericViewSet, CreateModelMixin):
    queryset = CustomUser.objects.all()
    serializer_class = CreateUserSerializer


class CurrentUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: UserSerializer()})
    @handle_exceptions
    def get(self, request: Request) -> Response:
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReferredUserViewSet(GenericViewSet, ListModelMixin):
    queryset = CustomUser.objects.all()
    serializer_class = ReferredUserSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request: Request, *args, **kwargs):
        user = request.user
        self.queryset = CustomUser.objects.filter(referred_by=user.referral_code)
        return super().list(request, *args, **kwargs)
