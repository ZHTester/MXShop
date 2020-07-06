"""MXShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
import xadmin

from django.conf.urls import url,include
from django.urls import path
from django.views.static import serve
from MXShop.settings import MEDIA_ROOT
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token
from goods.views import GoodsListViewSet,CategoryViewSet,BannerViewset,IndexCategoryViewSet
from users.views import SmsCodeViewset,UserViewset
from user_operation.views import UserFavViewset,LeavingMessageViewset,AddressViewset
from trade.views import ShoppingCartViewset,OrderViewset


# 配置goods的url
router = DefaultRouter()  # 首先生成一个router对象
# 商品列表  商品详情页 商品删除页 商品update页面
router.register(r'goods', GoodsListViewSet)
# 商品分类 url
router.register(r'categorys', CategoryViewSet)
# 用户发送验证码 url
router.register(r'codes', SmsCodeViewset)
# 用户注册 url
router.register(r'users', UserViewset)
# 用户收藏 url
router.register(r'userfavs', UserFavViewset)
# 用户留言
router.register(r'messages', LeavingMessageViewset)
# 用户收货地址
router.register(r'address', AddressViewset)
# 购物车
router.register(r'shopcarts', ShoppingCartViewset)
# 订单列表
router.register(r'orders', OrderViewset)
# banner
router.register(r'banners', BannerViewset)
# banner
router.register(r'indexgoods', IndexCategoryViewSet)


urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),   # 查找静态上传文件路径
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),  # drf登陆入口 后台登陆URL模块

    # 商品列表 restful的设计规范就是名词的复数形式
    # url(r'goods/$',goods_list,name='goods-list'),
    path('', include(router.urls)),

    # 安装coreapi生成drf文档功能
    url(r'docs/',include_docs_urls(title='我的DRF文档')),  # 这里就会自动去找到 coreapi 文档的存放地址了

    # 获取token  drf自带的认证模式
    url(r'^api-token-auth/', views.obtain_auth_token),

    # drf-jwt认证模式
    url(r'^login', obtain_jwt_token),
]
