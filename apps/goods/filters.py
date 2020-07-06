# encoding: utf-8

"""
# @Time    : 29/12/2019 11:35 上午
# @Author  : Function
# @FileName    : filters.py
# @Software: PyCharm

自定义过滤器查找类  这个是从价格中获取的数据
"""
from rest_framework import generics
from django_filters import rest_framework as filters  # 字段过滤
from django.db.models import Q
from .models import Goods


class GoodsFilter(filters.FilterSet):
    """
    商品列表 - 字段过滤Filter过滤
    """
    pricemin = filters.NumberFilter(field_name="shop_price", help_text='最低价格', lookup_expr='gte')
    pricemax = filters.NumberFilter(field_name="shop_price", lookup_expr='lte')
    name = filters.CharFilter(field_name="name",lookup_expr='contains')
    top_category = filters.NumberFilter(method='top_category_filter')  # 三级目录查找商品类别


    # 自定义方法过滤方法
    @staticmethod
    def top_category_filter(queryset, name, value):
        # 三级目录查找方式 过滤器 查找第一类别中的数据 双下划线和单下划线的区别
        return queryset.filter(Q(category_id=value)|Q(category__parent_category_id=value)|Q(category__parent_category__parent_category_id=value))

    class Meta:
        # 需要过滤的字段  是否是热销产品  是否是最新产品
        model = Goods
        fields = ['pricemin', 'pricemax', 'is_hot', 'is_new']




















