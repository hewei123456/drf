# -*- coding: utf-8 -*-
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token
from .models import UserProfile as User


class UserInfoSerializer(serializers.ModelSerializer):
    """
    用户信息
    """

    IDENTITY = (
        (1, '普通管理员'),
        (2, '超级管理员')
    )
    username = serializers.CharField(label='用户名', read_only=True)
    token = serializers.SerializerMethodField(label='令牌', read_only=True)
    identity = serializers.SerializerMethodField(label='身份', read_only=True)

    def get_token(self, user):
        token, created = Token.objects.get_or_create(user=user)
        return token.key

    def get_identity(self, user):
        return ('普通管理员', '超级管理员')[user.identity - 1]

    class Meta:
        model = User
        fields = ('identity', 'username', 'mobile', 'name', 'gender', 'email', 'avatar', 'token')


class UserRegSerializer(serializers.ModelSerializer):
    """
    用户注册
    """
    password = serializers.CharField(
        max_length=30,
        required=True,
        write_only=True,
        label='密码',
        style={'input': 'password'}
    )
    username = serializers.CharField(
        max_length=11, min_length=11, required=True, allow_blank=False, label='电话',
        validators=[
            UniqueValidator(queryset=User.objects.all(), message='用户名已存在')
        ],
        error_messages={
            'required': '请输入手机号',
            'blank': '请输入手机号',
            'max_length': '请输入十一位手机号',
            'min_length': '请输入十一位手机号'
        }
    )

    def create(self, validated_data):
        user = super(UserRegSerializer, self).create(validated_data=validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('username', 'password')
