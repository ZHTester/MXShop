from .serializers import GoodsSerializer,CategorySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from rest_framework.authentication import TokenAuthentication

from django_filters.rest_framework import DjangoFilterBackend
from .models import Goods,GoodsCategory,Banner
from .filters import GoodsFilter
from .serializers import BannerDSerializer,IndexCategorysSerializer
"""
1 接收前段传递的数据将它装换成json数据格式保存到数据库中
2 PageNumberPagination - 定制分页类型继承类型
"""
class GoodsPagination(PageNumberPagination):
    """
    分页查询
    """
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100

class GoodsListViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
# class GoodsListViewSet(APIView):
# class GoodsListViewSet(mixins.ListModelMixin,generics.GenericAPIView):
# class GoodsListViewSet(generics.ListAPIView):
    """
    接口描述
    商品列表接口 【分页  搜索  过滤 排序】
    mixins.RetrieveModelMixin 获取商品详情页面数据
    """
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    # # 单独认证token的方式 在view中进行
    # authentication_classes = (TokenAuthentication,)
    pagination_class = GoodsPagination

    # 配置过滤器  字段过滤器 搜索器 排序
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = GoodsFilter
    search_fields = ('name', 'goods_brief', 'goods_desc')
    ordering_fields = ('sold_num', 'shop_price')

    # def get_queryset(self):
    #     """
    #     过滤器
    #     :return:
    #     """
    #     queryset = Goods.objects.all()  # 首先是获取到所有的执行脚本文件
    #     price_min = self.request.query_params.get("price_min", 0)  #前段获取数据
    #     if price_min:
    #         queryset = Goods.objects.filter(shop_price__gt=price_min)
    #     return queryset

    # def get(self, request, *args, **kwargs):
    #     """
    #     默认接收这样的方法 也就是不接受这样的请求
    #     :param request:
    #     :param args:
    #     :param kwargs:
    #     :return:
    #     """
    #     return self.list(request, *args, **kwargs)

    # def get(self, request, format=None):
    #     goods = Goods.objects.all()[:10]
    #     goods_serializer = GoodsSerializer(goods, many=True)  # 代表的是一个list对象 数据序列化
    #     from rest_framework.response import Response 使用的是drf的response对象
    #     return Response(goods_serializer.data)  # 返回序列化数据列表对象

    # def post(self,request,format=None):
    #     """
    #     进行上传数据的操作 也就是用户提交操作
    #     :param request:
    #     :param format:
    #     :return:
    #     """

    #     # 进行数据验证获取所有的数据 这里就不用判断是get还是post方法
    #     serializer = GoodsSerializer(data=request.data)
    #     # 对数据进行验证返回
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)  # 保存成功返回201
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:
        商品分类列表数据
    # 获取到数据的详情页面数据 关键是url的配置是如何配置的
    # mixins.RetrieveModelMixin 获取商品的详情数据 的接口数据
    """
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer

class BannerViewset(mixins.ListModelMixin,viewsets.GenericViewSet):
    """
    商品轮播图
    """
    queryset = Banner.objects.all().order_by('index')
    serializer_class = BannerDSerializer


class IndexCategoryViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):
    queryset = GoodsCategory.objects.filter(is_tab=True,name__in=["生鲜食品", "酒水饮料"])
    serializer_class = IndexCategorysSerializer

