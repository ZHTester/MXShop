# encoding: utf-8

"""
# @Time    : 12/4/2020 5:33 下午
# @Author  : Function
# @FileName    : base_views.py
# @Software: PyCharm
"""
import json
from django.views.generic.base import View
from django.http import HttpResponse,JsonResponse
from django.forms.models import model_to_dict
from django.core import serializers  # serializers 序列化

from .models import UserProfile



class GoodsViews(View):
    def get(self,request):
        """
        通过Django-view 实现商品列表页面的数据获取
        :param request:
        :return:
        """
        users = UserProfile.objects.all()  # 获取页面数据
        json_list =[]
        # for us in users:
            ## 常规写法 返回json格式
            # # 循环出数据
            # dict_json = {'name': us.name, 'last-name': us.last_name}
            # json_list.append(json_list)

            ## 返回json数据在浏览器上展示数据
            # return  HttpResponse(json.dumps(dict_json),content_type='application/json')
            ## model_to_dict 字典json转换格式
            # json_dict = model_to_dict(us)
            # json_list.append(json_dict)

        ## serializers 序列化写法
        json_data = serializers.serialize('json',users)
        json_data = json.loads(json_data)
        return  JsonResponse(json_data,safe=False)

























