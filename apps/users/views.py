from django.contrib.auth.backends import ModelBackend
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.mixins import CreateModelMixin
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import permissions  # 权限
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import authentication
from rest_framework.response import Response
from rest_framework import status
from .serializers import SmsSerializers
from utils.yunpian import YunPian
from MXShop.settings import APIKEY
from random import choice
from .models import VerifyCode
from .serializers import UserRegSerializers,UserDetailSerializer
from rest_framework_jwt.serializers import jwt_encode_handler,jwt_payload_handler
# Create your views here.


User = get_user_model()
class CustomBackend(ModelBackend):
    """
     自定义用户认证方式
     用户名 邮箱登陆方式验证

    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(mobile=username))  # 并集的操作
            if user.check_password(password):
                return user
        except Exception as e:
            return None

class SmsCodeViewset(CreateModelMixin,viewsets.GenericViewSet):
    """
    手机短信发送接口
    """
    queryset = VerifyCode.objects.all()
    serializer_class = SmsSerializers

    def generic_code(self):
        """
         生成4位数字的验证码
        :return:
        """
        seeds = '1234567890'
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))

    def create(self, request, *args, **kwargs):
        """
         重写create方法  用户登陆生成
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data["mobile"]  # 取出手机号
        yunpan = YunPian(APIKEY)

        sms_status = yunpan.send_sms(code=self.generic_code(),mobile=mobile)  # 发送手机短信 返回的状态吗 后面需要对状态吗进行判断

        if sms_status['code'] != 0:
            return Response({
                    "mobile":sms_status['msg']
                },status=status.HTTP_400_BAD_REQUEST)
        else:
            code_record = VerifyCode(code=self.generic_code(),mobile=mobile)
            code_record.save() # 保存数据库
            return Response({
                    "mobile":mobile
                },status=status.HTTP_201_CREATED
            )


class UserViewset(CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    用户注册
    用户修改
    用户信息获取      
    """
    serializer_class = UserRegSerializers
    queryset = User.objects.all()
    authentication_classes = (authentication.SessionAuthentication,JSONWebTokenAuthentication)  # session管理  用户权限管理

    """
    1 注册完成后 完成登陆的操作 并且跳转到首页
    2 生成用户的Token之前是需要拿到用户的User
    mixins.RetrieveModelMixin 获取当个实例
    """

    def get_serializer_class(self):
        """
        返回用户详情或者注册详情
        动态获取serializer
        :return:
        """
        if self.action == "retrieve":
            return UserDetailSerializer
        elif self.action == "create":
            return UserRegSerializers

        return UserDetailSerializer

    # permission_classes = (permissions.IsAuthenticated,)  # 相关登陆权限 动态赋权限
    def get_permissions(self):
        """
        动态配置权限 如果是get post请求就需要权限dengue  在APIVIEW中的重写函数
        :return:
        """
        if self.action == "retrieve":
            return [permissions.IsAuthenticated()]
        elif self.action == "create":
            return []

        return []


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        re_dict = serializer.data  # 获取整体的数据
        payload = jwt_payload_handler(user)
        re_dict['token'] = jwt_encode_handler(payload)
        re_dict['name'] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def get_object(self):
        """
        返回当前用户 必须是登陆的状态
        :return:
        """
        return self.request.user

    def perform_create(self, serializer):
        return serializer.save()




