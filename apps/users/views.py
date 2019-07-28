from django.shortcuts import render
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from rest_framework import status, authentication
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.mixins import (ListModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin)
from rest_framework.authtoken.models import Token

from .models import UserProfile as User
from .serializers import UserRegSerializer, UserInfoSerializer


# Create your views here.
class CustomBackend(ModelBackend):
    """
    自定义登录后台
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(mobile=username) | Q(username=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class UserViewSet(CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    """
    create:
        注册用户
    list:
        用户信息
    update:
        修改信息
    """
    authentication_classes = (authentication.TokenAuthentication, authentication.SessionAuthentication)
    serializer_class = UserRegSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegSerializer
        else:
            return UserInfoSerializer

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    def get_permissions(self):
        if self.action == 'create':
            return []
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        re_dict = serializer.data
        token = Token.objects.create(user=user)
        re_dict['token'] = str(token)
        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()
