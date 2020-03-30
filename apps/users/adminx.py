# encoding: utf-8

"""
# @Time    : 25/12/2019 3:15 下午
# @Author  : Function
# @FileName    : adminx.py
# @Software: PyCharm
"""
import xadmin
from .models import UserProfile,VerifyCode

class UserProfileAdmin:
    """
    用户收藏
    """
    list_display = ['name','birthday','gender','mobile','email']  # 书签
    search_fields = ['name','birthday','gender','mobile','email']  # 搜索框
    list_filter = ['name','birthday','gender','mobile','email']  # 过滤器

class VerifyCodeAdmin:
    """
    用户留言信息
    """

    list_display = ['code','mobile','add_time']
    search_fields = ['code','mobile','add_time']
    list_filter = ['code','mobile','add_time']

xadmin.site.unregister(UserProfile)
xadmin.site.register(UserProfile,UserProfileAdmin)
xadmin.site.register(VerifyCode,VerifyCodeAdmin)

