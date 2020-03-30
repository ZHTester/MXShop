from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    """
    用户
    """
    name = models.CharField(verbose_name=u'姓名',max_length=100,null=True,blank=True)
    birthday = models.DateField(verbose_name='出生年月',null=True,blank=True)
    gender = models.CharField(verbose_name=u'性别',max_length=20,choices=(("male",u"男"),("female","女")),default='female')
    mobile = models.CharField(null=True,blank=True,max_length=11,verbose_name=u'电话')
    email = models.EmailField(max_length=100,null=True,blank=True,verbose_name=u'邮箱')

    class Meta:
        verbose_name = u'用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

class VerifyCode(models.Model):
    """
    短信验证码
    """
    code = models.CharField(max_length=100,verbose_name=u'验证码')
    mobile = models.CharField(max_length=11, verbose_name=u'电话')
    add_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')

    class Meta:
        verbose_name = u'验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code