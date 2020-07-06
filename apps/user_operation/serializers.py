# encoding: utf-8

"""
# @Time    : 6/2/2020 11:00 上午
# @Author  : Function
# @FileName    : serializers.py
# @Software: PyCharm
"""
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator  # 字段唯一性验证
from .models import UserFav,UserLeavingMessage,UserAddress
from goods.serializers import GoodsSerializer

class UserFavDetailSerializer(serializers.ModelSerializer):
    """
    用户收藏商品详情页面
    """
    goods = GoodsSerializer()
    class Meta:
        model = UserFav
        fields = ('goods','id')

class UserFavSerializer(serializers.ModelSerializer):
    """
    1 用户商品收藏功能
    2 如果是需要返回删除功能这个时候我们就需要返回id
    """
    # 默认显示当前用户不在前端显示
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        # 同一数据唯一性验证  收藏功能
        model= UserFav
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=['user', 'goods'],
                message = "已经收藏"  # 错误返回消息
            )
        ]
        fields = ("user","goods","id")

class LeavingMessageSerializer(serializers.ModelSerializer):
    """
    用户留言
    """
    # 默认当前用户 且前端不显示当前用户
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True,format='%Y-%m-%d  %H:%M')

    class Meta:
        model = UserLeavingMessage
        fields = ('user','message_type','subject','message','file','id','add_time')


class UserAddressSerializer(serializers.ModelSerializer):
    """
    用户地址

    """
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d  %H:%M')

    class Meta:
        model = UserAddress
        fields = ('user', 'province', 'city', 'district', 'address', 'signer_name', 'signer_mobile','add_time','id')



