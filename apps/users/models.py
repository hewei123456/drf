from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class UserProfile(AbstractUser):
    IDENTITY = (
        (1, '普通管理员'),
        (2, '超级管理员')
    )
    identity = models.IntegerField(default=1, choices=IDENTITY, verbose_name='角色')
    name = models.CharField(max_length=10, null=True, blank=True, verbose_name='姓名')
    gender = models.IntegerField(default=1, choices=((1, '男'), (2, '女')), verbose_name='性别')
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name='电话号码')
    avatar = models.ImageField(null=True, blank=True, upload_to='users/avatars/', verbose_name='头像')

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.name)
