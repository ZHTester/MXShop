# encoding: utf-8

"""
# @Time    : 27/12/2019 5:37 下午
# @Author  : Function
# @FileName    : serializer.py
# @Software: PyCharm

Serializer  是直接转换成json格式的比modelFrom更加的强大  是用来取代常规的 Modlefrom 数据转换成Html
"""
from django.db.models import Q
from rest_framework import serializers

from .models import Goods,GoodsCategory,GoodsImage,Banner,GoodsCategoryBrand,IndexAd
"""
3层嵌套数据 商品类别序列化
"""
class CategorySerializer3(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer2(serializers.ModelSerializer):
    sub_cat = CategorySerializer3(many=True)
    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    sub_cat = CategorySerializer2(many=True)
    class Meta:
        model = GoodsCategory
        fields = "__all__"

class GoodsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsImage
        fields = ("image",)
"""
商品数据序列化
"""
class GoodsSerializer(serializers.ModelSerializer):
    """
    商品详情页面显示
    """
    # name = serializers.CharField(required=True,max_length=100)
    # click_num = serializers.IntegerField(default=0)
    # goods_front_image = serializers.ImageField()
    category = CategorySerializer()   # Goods 中嵌套
    images = GoodsImageSerializer(many=True)  # 嵌套显示数据方式
    class Meta:
        model = Goods
        fields = '__all__'

    # def create(self, validated_data):
    #     """
    #     Create and return a new `GOODS` instance, given the validated data.
    #     """
    #     return Goods.objects.create(**validated_data)  # Object相当于一个drf的管理器 创建一个drf对象

class BannerDSerializer(serializers.ModelSerializer):
    """
    商品轮播图
    """
    class Meta:
        model = Banner
        fields = "__all__"

class BrandSerializer(serializers.ModelSerializer):
    """
    商品名称
    """
    class Meta:
        model =  GoodsCategoryBrand
        fields = '__all__'

class IndexCategorysSerializer(serializers.ModelSerializer):
    """
     首页商品分类
    """
    brands = BrandSerializer(many=True)
    goods = serializers.SerializerMethodField()
    sub_cat = CategorySerializer2
    ad_goods = serializers.SerializerMethodField()

    def get_ad_goods(self, obj):
        goods_json = {}
        ad_goods = IndexAd.objects.filter(category_id=obj.id, )
        if ad_goods:
            good_ins = ad_goods[0].goods
            goods_json = GoodsSerializer(good_ins, many=False, context={'request': self.context['request']}).data
        return goods_json

    def get_goods(self,obj):
        all_goods = Goods.objects.filter(Q(category_id=obj.id)|Q(category__parent_category_id=obj.id)|
                                         Q(category__parent_category__parent_category_id=obj.id))
        goods_serializer = GoodsSerializer(all_goods, many=True, context={'request': self.context['request']})
        return goods_serializer.data

    class Meta:
        model =  GoodsCategory
        fields = '__all__'
