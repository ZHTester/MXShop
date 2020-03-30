# encoding: utf-8

"""
# @Time    : 25/12/2019 3:15 下午
# @Author  : Function
# @FileName    : adminx.py
# @Software: PyCharm
"""
import xadmin
from .models import GoodsCategory,GoodsCategoryBrand,Goods,GoodsImage,Banner
from .models import IndexAd

class GoodsCategoryAdmin:
    """
    商品类别 一对多的关系
    """
    list_display = ['name','code','desc','category_type','add_time']  # 书签
    search_fields = ['name','code','desc','category_type']  # 搜索框
    list_filter = ['name','code','desc','category_type','add_time']  # 过滤器

class GoodsCategoryBrandAdmin:
    """
    品牌名称
    """
    list_display = ['category','name','desc','image','add_time']
    search_fields = ['category','name','desc','add_time']
    list_filter = ['category','name','desc','add_time']

class GoodsAdmin:
    """
    商品
    """
    list_display = ['category','good_sn','name','click_num','sold_num','fav_num','goods_num','market_price','shop_price',
                    'goods_brief','ship_free','goods_front_image','is_new','is_hot','add_time']
    search_fields = ['category','good_sn','name','click_num','sold_num','fav_num','goods_num','market_price','shop_price',
                    'goods_brief','ship_free','goods_front_image','is_new','is_hot','add_time']
    list_filter = ['category','good_sn','name','click_num','sold_num','fav_num','goods_num','market_price','shop_price',
                    'goods_brief','ship_free','goods_front_image','is_new','is_hot','add_time']

class GoodsImageAdmin:
    """
    轮播商品图
    """
    list_display = ['goods','image_url','add_time']
    search_fields = ['goods','image_url','add_time']
    list_filter = ['goods','image_url','add_time']


class GoodsBrandAdmin(object):
    list_display = ["category", "image", "name", "desc"]

    def get_context(self):
        context = super(GoodsBrandAdmin, self).get_context()
        if 'form' in context:
            context['form'].fields['category'].queryset = GoodsCategory.objects.filter(category_type=1)
        return context

class BannerAdmin(object):
    list_display = ["goods", "image", "index"]


class HotSearchAdmin(object):
    list_display = ["keywords", "index", "add_time"]


class IndexAdAdmin(object):
    list_display = ["category", "goods"]


xadmin.site.register(Banner,BannerAdmin)
xadmin.site.register(GoodsImage,GoodsImageAdmin)
xadmin.site.register(Goods,GoodsAdmin)
xadmin.site.register(GoodsCategory,GoodsCategoryAdmin)
xadmin.site.register(GoodsCategoryBrand,GoodsCategoryBrandAdmin)

xadmin.site.register(IndexAd,IndexAdAdmin)
