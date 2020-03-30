# encoding: utf-8

"""
# @Time    : 27/12/2019 3:46 下午
# @Author  : Function
# @FileName    : view_base.py
# @Software: PyCharm

使用常规的Django的方式进行书写View 完成json的返回
1 获取到所有数据也就是提取出数据库中所有字段
2 在进行数据转换转换成一个json格式
3 模块化的序列化操作
4 将modle的对象转换成一个dict对象将所有的字段全部都提取出来   from django.forms.models import model_to_dict
"""
from django.views.generic.base import View
from .models import Goods

class GoodsListView(View):
    def get(self,request):

        json_list = []
        goods = Goods.objects.filter()[:10]
        # for good in goods:
        #     json_dict = {}
        #     json_dict['name'] = good.name
        #     json_dict['category'] = good.category.name
        #     json_dict['market_price'] = good.market_price
        #     json_list.append(json_dict)
        import json

        # 直接返回所有数据的序列化 提取出所有数据  直接序列化+list返回数据
        from django.core import serializers
        json_data = serializers.serialize('json',goods)
        json_data = json.loads(json_data)

        from django.forms.models import model_to_dict
        # 只是单纯的序列化数据而已 没有进行list排序 这里还是需要一个append进行胶乳操作
        # for good in goods:
        #     json_dict = model_to_dict(good)
        #     json_list.append(json_dict)
        from django.http import HttpResponse,JsonResponse

        # return HttpResponse(json.dumps(json_data),content_type="application/json")
        return JsonResponse(json_data,safe=False)  # 返回数据格式就是json格式数据类型



