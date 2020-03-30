# encoding: utf-8

"""
# @Time    : 13/2/2020 11:00 上午
# @Author  : Function
# @FileName    : serializers.py
# @Software: PyCharm
"""
import time
from rest_framework import serializers
from goods.models import Goods,Banner
from .models import ShoppingCart,OrderInfo,OrderGoods
from goods.serializers import GoodsSerializer

class OrderGoodsSerializer(serializers.ModelSerializer):
    """
    商品订单详情页面
    """
    goods = GoodsSerializer(many=False)
    class Meta:
        model = OrderGoods
        fields = "__all__"

class OrderDetailSerializer(serializers.ModelSerializer):
    """
     订单详情页面
    """
    goods = OrderGoodsSerializer(many=True)
    class Meta:
        model = OrderInfo
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    """
    个人订单中心
    """
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    pay_status = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    order_sn = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True)

    def generate_order_sn(self):
        """
        生成订单号唯一标示 生成的订单号就可以保证是唯一的
        :return:
        """
        from random import Random
        random_ins = Random()
        order_sn = "{time_str}{userid}{ranstr}".format(time_str=time.strftime("%Y%m%d%H%M%S"),
                                                       userid=self.context["request"].user.id,
                                                       ranstr=random_ins.randint(10, 99))
        return order_sn

    def validate(self, attrs):
        """
        数据验证 生成订单号
        :param attrs:
        :return:
        """
        attrs['order_sn'] = self.generate_order_sn()
        return attrs

    class Meta:
        model = OrderInfo
        fields = "__all__"

class ShopCartDetailSerializer(serializers.ModelSerializer):
    """
    商品购物车详情页面
    """
    goods = GoodsSerializer(many=False)
    class Meta:
        model = ShoppingCart
        fields = ("goods", "nums")

class ShoppingSerializer(serializers.Serializer):
    """
     商品列表购物车
    """
    # 默认当前用户 且前端不显示当前用户
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    nums = serializers.IntegerField(required=True,min_value=1,
                                    error_messages={
                                        "min_value": "商品数量不能小于一",
                                        "required": "请选择购买数量"
                                    })
    goods = serializers.PrimaryKeyRelatedField(required=True, queryset=Goods.objects.all())

    def create(self, validated_data):
        """
         创建商品 新增
        :param validated_data:
        :return:
        """
        user = self.context['request'].user
        nums =  validated_data['nums']
        goods = validated_data['goods']

        existed = ShoppingCart.objects.filter(user=user, goods=goods)

        if existed:
            existed = existed[0]
            existed.nums += nums
            existed.save()

        else:
            existed = ShoppingCart.objects.create(**validated_data)

        return existed

    def update(self, instance, validated_data):
        """
        更新购物车数量
        :param instance:
        :param validated_data:
        :return:
        """
        instance.goods_num =validated_data['nums']
        instance.save()
        return instance





