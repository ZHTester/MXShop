# encoding: utf-8

"""
# @Time    : 25/12/2019 3:15 下午
# @Author  : Function
# @FileName    : adminx.py
# @Software: PyCharm
"""
import xadmin
from .models import UserFav,UserLeavingMessage,UserAddress

class UserFavAdmin:
    """
    用户收藏
    """
    list_display = ['user','goods','add_time']  # 书签

class UserLeavingMessageAdmin:
    """
    用户留言信息
    """
    list_display = ['user','message_type','subject','message','file','add_time']

class UserAddressAdmin:
    """
    用户收获地址
    """
    list_display = ['user','province','city','district','address','signer_name','signer_mobile','add_time']

xadmin.site.register(UserFav,UserFavAdmin)
xadmin.site.register(UserLeavingMessage,UserLeavingMessageAdmin)
xadmin.site.register(UserAddress,UserAddressAdmin)

