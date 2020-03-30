# encoding: utf-8

"""
# @Time    : 22/1/2020 10:00 上午
# @Author  : Function
# @FileName    : serializers.py
# @Software: PyCharm
"""
import re
from datetime import datetime
from datetime import timedelta

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import VerifyCode
from rest_framework.validators import UniqueValidator


User = get_user_model()


class SmsSerializers(serializers.Serializer):
    """
    用户发送短信
    """
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        """
        手机号码验证
        :param mobile:
        :return:
        """
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError('用户已经存在')

        if re.match(r'^1[35789]\d{9}$',mobile):
            raise  serializers.ValidationError('手机号码非法')

        one_minutes_ago = datetime.now() - timedelta(hours=0,minutes=1,seconds=0)
        if VerifyCode.objects.filter(add_time__gte=one_minutes_ago,mobile=mobile).count():
            raise serializers.ValidationError('距离上一次分送为超过60秒')

        return mobile

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("name", "gender", "birthday", "email", "mobile")

class UserRegSerializers(serializers.ModelSerializer):
    """
    user 注册验证功能 发送短信验证码
    """
    # 声明一个code的 serializers
    code = serializers.CharField(required=True,max_length=4,write_only=True,min_length=4,help_text='验证码',label=u'验证码'
                                 ,error_messages={
            "blank":"请输入验证码",
            "required": "请输入验证码",
            "min_length": "验证码格式错误",
            "max_length": "验证码格式错误"

        })

    # 密码设置
    password = serializers.CharField(
        style={'input_type': 'password'},label='密码',write_only=True
    )

    username = serializers.CharField(label='用户名',required=True,allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all())])  # 判断唯一性 字段

    def validate_code(self, code):
        """
        code验证 作用于code这个字段之上的一个校验
        :param code:
        :return:
        """
        # 前端获取传入的手机号 并且进行安装时间排序
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data['username']).order_by('-add_time')
        if verify_records:
            last_records = verify_records[0]

            # 验证验证码时间过期
            five_minutes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if five_minutes_ago > last_records.add_time:
                raise serializers.ValidationError('验证码过期')

            # 验证码错误 验证码不相等
            if last_records.code != code:
                raise serializers.ValidationError('验证码错误')

        else:
            raise serializers.ValidationError('验证码错误')

    def validate(self, attrs):
        """
        作用域所有字段之上
        :param self:
        :param attrs:  每个字段返回的所有总的dict
        :return:
        """
        attrs['mobile'] = attrs['username']
        del attrs['code']
        return attrs

    class Meta:
        model = User
        fields = ['username','code','mobile','password']