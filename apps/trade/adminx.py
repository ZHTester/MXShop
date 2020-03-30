# encoding: utf-8

"""
# @Time    : 25/12/2019 3:15 下午
# @Author  : Function
# @FileName    : adminx.py
# @Software: PyCharm
"""
import xadmin
from .models import ShoppingCart,OrderInfo,OrderGoods

class ShoppingCartAdmin:
    """
    购物车
    """
    list_display = ['user','goods','goods_num','add_time']  # 书签
    search_fields = ['user','goods','goods_num']   # 搜索框
    # list_filter = ['user','goods','goods_num','add_time']   # 过滤器

class OrderInfoAdmin:
    """
    订单
    """
    list_display = ['user','order_sn','trade_no','post_script','post_script',
                    'pay_time','address','signer_name']
    search_fields = ['user','order_sn','trade_no','pay_status','post_script','post_script',
                    'order_mount','pay_time','address','signer_name']

class OrderGoodsAdmin:
    """
    订单的商品详情
    """
    list_display = ['order','goods','goods_num','add_time']
    search_fields = ['order','goods','goods_num','add_time']
    list_filter =['order','goods','goods_num','add_time']


xadmin.site.register(ShoppingCart,ShoppingCartAdmin)
xadmin.site.register(OrderInfo,OrderInfoAdmin)
xadmin.site.register(OrderGoods,OrderGoodsAdmin)
