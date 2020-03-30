from django.apps import AppConfig


class UserOperationConfig(AppConfig):
    name = 'user_operation'
    verbose_name = '用户操作管理'

    def ready(self):
        # 信号量注册
        import user_operation.signals