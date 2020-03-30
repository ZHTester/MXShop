# encoding: utf-8
"""
# @Time    : 27/3/2020 3:10 下午
# @Author  : Function
# @FileName    : weibo_login.py
# @Software: PyCharm

weibo 《---》 登陆工具类
具体登陆方式请参看微博开放平台

"""
def get_auth_url():
    """
    微博登陆授权APi方法
    :return:
    """
    weibo_auth_url = 'https://api.weibo.com/oauth2/authorize'  # weiboAPI 地址
    weibo_redirect_url = 'https://47.92.87.172:8000/complete/weibo'  # weibo回掉函数
    auth_url = weibo_auth_url+"?client_id={client_id}&redirect_uri={re_uri}".format(client_id=237999617,re_uri=weibo_redirect_url)

    print(auth_url)

if __name__ == '__main__':
    get_auth_url()



