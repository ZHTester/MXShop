# encoding: utf-8

"""
# @Time    : 29/1/2020 3:36 下午
# @Author  : Function
# @FileName    : signals.py
# @Software: PyCharm

修改用户密码 信号量

"""
from django.conf import settings
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from user_operation.models import UserFav

@receiver(post_save, sender=UserFav)
def create_userfav(sender, instance=None, created=False, **kwargs):
    if created:
        # 修改用户信号量
        goods = instance.goods
        goods.fav_num +=1
        goods.save()


@receiver(post_delete, sender=UserFav)
def delete_userfav(sender, instance=None, created=False, **kwargs):
    if created:
        # 修改用户信号量
        goods = instance.goods
        goods.fav_num -=1
        goods.save()

