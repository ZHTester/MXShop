from django.shortcuts import render
import time
from rest_framework_jwt.authentication import JSONWebTokenAuthentication  # 用户token
from rest_framework.authentication import SessionAuthentication  # 用户session
from utils.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework import mixins
from .serializers import ShoppingSerializer, ShopCartDetailSerializer, OrderSerializer,OrderDetailSerializer
from .models import ShoppingCart,OrderGoods,OrderInfo


class ShoppingCartViewset(viewsets.ModelViewSet):
    """
      购物车功能
      list:
          获取购物车详情
      create：
          加入购物车
      delete：
          删除购物记录
      """
    permission_classes = (IsAuthenticated,IsOwnerOrReadOnly)  # 权限验证
    authentication_classes = (JSONWebTokenAuthentication,SessionAuthentication)   # 登陆token验证 不会在全局做json的验证
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingSerializer
    lookup_field = "goods_id"

    def perform_create(self, serializer):
        # 增加操作
        shop_care = serializer.save()
        goods = shop_care.goods
        goods.goods_num -= shop_care.nums
        goods.save()

    def perform_destroy(self, instance):
        # 删除操作
        goods = instance.delete()
        goods.goods_num += instance.nums
        goods.save()
        instance.delete()

    def perform_update(self, serializer):
        # 更新操作
        existed_record = ShoppingCart.objects.get(id=serializer.instance.id)
        existed_nums = existed_record.nums
        saved_record = serializer.save()
        nums = saved_record.nums - existed_nums
        goods = saved_record.goods
        goods.goods_num -= nums
        goods.save()

    def get_serializer_class(self):
        """
        购物车商品详情页面动态现实
        :return:
        """
        if self.action == 'list':
            return ShopCartDetailSerializer
        else:
            return ShoppingSerializer

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)

class OrderViewset(mixins.ListModelMixin,mixins.CreateModelMixin,mixins.DestroyModelMixin,mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    """
    订单列表
      list:
          获取个人订单
      create：
          删除订单
      delete：
          新增订单
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)  # 权限验证
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)  # 登陆token验证 不会在全局做json的验证
    queryset = OrderInfo.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        """
        获取到自己本身的订单信息
        :return:
        """
        return OrderInfo.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return OrderDetailSerializer
        return OrderSerializer

    def perform_create(self, serializer):
        """
        保存实列
        :param serializer:
        :return:
        """
        order = serializer.save()

        # 生成订单
        shop_carts = ShoppingCart.objects.filter(user=self.request.user)
        for shop_cart in shop_carts:
            order_goods = OrderGoods()
            order_goods.goods = shop_cart.goods
            order_goods.goods_num = shop_cart.nums
            order_goods.order = order
            order_goods.save()
            # 清空购物车
            shop_cart.delete()
        return order






