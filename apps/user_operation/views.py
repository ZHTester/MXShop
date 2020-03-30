from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication  # 用户token
from rest_framework.authentication import SessionAuthentication  # 用户session
from utils.permissions import IsOwnerOrReadOnly
from .models import UserFav,UserLeavingMessage,UserAddress
from .serializers import UserFavSerializer,UserFavDetailSerializer,LeavingMessageSerializer,UserAddressSerializer


class UserFavViewset(mixins.CreateModelMixin,mixins.ListModelMixin,mixins.DestroyModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    """
    用户收藏功能 添加 删除 权限
    mixins.CreateModelMixin 新增收藏
    mixins.DestroyModelMixin 删除收藏 取消收藏
    mixins.ListModelMixin 获取收藏商品列表功能
    mixins.RetrieveModelMixin 商品号回生成一个Url
    list:
        获取商品收藏列表
    create:
        新增商品收藏
    retrieve:
        收藏商品
    """
    queryset = UserFav.objects.all()
    permission_classes = (IsAuthenticated,IsOwnerOrReadOnly)  # 权限验证
    authentication_classes = (JSONWebTokenAuthentication,SessionAuthentication)   # 登陆token验证 不会在全局做json的验证
    lookup_field = "goods_id"

    def get_serializer_class(self):
        """
        返回用户详情或者注册详情
        动态获取serializer
        :return:
        """
        if self.action == "list":
            return UserFavDetailSerializer
        elif self.action == "create":
            return UserFavSerializer

        return UserFavSerializer

    serializer_class =  UserFavSerializer

    def get_queryset(self):
        # 显示自己的收藏
        return UserFav.objects.filter(user=self.request.user)

class LeavingMessageViewset(mixins.ListModelMixin, mixins.CreateModelMixin,
                            mixins.DestroyModelMixin,viewsets.GenericViewSet):
    """
    用户留言
    """
    queryset = UserLeavingMessage.objects.all()
    serializer_class = LeavingMessageSerializer
    permission_classes = (IsAuthenticated,IsOwnerOrReadOnly)  # 权限验证
    authentication_classes = (JSONWebTokenAuthentication,SessionAuthentication)   # 登陆token验证 不会在全局做json的验证

    def get_queryset(self):
        # 获取当前用户的留言xi
        return UserLeavingMessage.objects.filter(user=self.request.user)


class AddressViewset(viewsets.ModelViewSet):
    """
    收货地址管理
    list:
        获取收货地址
    create:
        添加收货地址
    update:
        更新收货地址
    delete:
        删除收货地址
    """
    queryset = UserAddress.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = UserAddressSerializer

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)