# encoding: utf-8

"""
# @Time    : 29/1/2020 3:36 下午
# @Author  : Function
# @FileName    : signals.py
# @Software: PyCharm

修改用户密码 信号量

"""
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        # 修改用户信号量
        password = instance.password
        instance.set_password(password)
        instance.save()

