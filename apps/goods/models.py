from datetime import datetime

from django.db import models
from DjangoUeditor.models import UEditorField

# Create your models here.


class GoodsCategory(models.Model):
    """
    商品类别 一对多的关系
    """
    GATEGORY_TYPE = (
        (1, "一级类目"),
        (2, "二级类目"),
        (3, "三级类目"),
    )
    name = models.CharField(verbose_name=u'类别名',default='',max_length=300,help_text=u'类别名')
    code = models.CharField(default='',verbose_name=u'类别code',max_length=200,help_text=u'类别code')
    desc = models.TextField(default='',verbose_name=u'类别描述',max_length=200,help_text=u'类别描述')
    category_type = models.IntegerField(choices=GATEGORY_TYPE, verbose_name="类目级别", help_text="类目级别")
    parent_category = models.ForeignKey("self", null=True, blank=True, verbose_name="父类目级别", help_text="父目录",
                                        related_name="sub_cat",on_delete=models.CASCADE)
    is_tab = models.BooleanField(default=False,verbose_name=u'是否导航',help_text=u'是否导航')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = u'商品类别'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class GoodsCategoryBrand(models.Model):
    """
    品牌名称
    """
    category = models.ForeignKey(GoodsCategory,null=True,blank=True,related_name='brands',verbose_name=u'商品类目',on_delete=models.CASCADE)
    name = models.CharField(default='',verbose_name=u'品牌名称',max_length=200)
    desc = models.TextField(default='',verbose_name=u'品牌描述',max_length=200,help_text=u'品牌描述')
    image = models.ImageField(upload_to='brands/')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = u'品牌名称'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Goods(models.Model):
    """
    商品

    """
    category = models.ForeignKey(GoodsCategory,verbose_name=u'商品类目',on_delete=models.CASCADE)
    good_sn = models.CharField(verbose_name=u'商品唯一货号',default='',max_length=200)
    name = models.CharField(verbose_name=u'商品名称',max_length=300)
    click_num = models.IntegerField(verbose_name='点击数',default=0)
    sold_num = models.IntegerField(verbose_name='商品销售数',default=0)
    fav_num = models.IntegerField(verbose_name='收藏数',default=0)
    goods_num = models.IntegerField(verbose_name='库存数',default=0)
    market_price = models.FloatField(default=0, verbose_name="市场价格")
    shop_price = models.FloatField(default=0, verbose_name="本店价格")
    goods_brief = models.TextField(max_length=1000,verbose_name=u'商品简单描述')
    goods_desc =UEditorField(verbose_name=u'内容',imagePath='goods/images/',width=1000,height=3000,filePath='goods/files/',default='')
    ship_free = models.BooleanField(default= True,verbose_name=u'是否承担运费')
    goods_front_image = models.ImageField(upload_to="goods/images/",null=True,blank=True,verbose_name=u'商品封面图')  # 商品封面图
    is_new = models.BooleanField(default=False,verbose_name=u'是否是新品')  # 判断是否是新品
    is_hot = models.BooleanField(default=False,verbose_name=u'是否是热卖') # 是否是热卖商品
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')


    class Meta:
        verbose_name = u"商品"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class IndexAd(models.Model):
    """
    首页商品类别广告
    """
    category = models.ForeignKey(GoodsCategory, verbose_name=u'商品类目',related_name='category', on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, verbose_name='商品', related_name='goods', on_delete=models.CASCADE)
    class Meta:
        verbose_name = u"首页商品类别广告"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name


class GoodsImage(models.Model):
    """
    商品轮播图
    """
    goods = models.ForeignKey(Goods,verbose_name='商品',related_name='images',on_delete=models.CASCADE)
    image = models.ImageField(upload_to='',verbose_name='图片',null=True,blank=True)
    image_url = models.CharField(max_length=300,null=True,blank=True,verbose_name=u'图片url')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = u'商品轮播图'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name

class Banner(models.Model):
    """
    轮播商品图
    """
    goods = models.ForeignKey(Goods,verbose_name=u'商品',on_delete=models.CASCADE)
    image = models.ImageField(upload_to='banner',verbose_name=u'轮播图片')
    index = models.IntegerField(default=0,verbose_name='轮播顺序')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = u'轮播商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name





