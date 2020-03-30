from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'
    verbose_name = '用户管理'

    def ready(self):
        # 信号量注册
        import users.signals