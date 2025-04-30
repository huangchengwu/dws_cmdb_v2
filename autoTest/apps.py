from django.apps import AppConfig


class AutotestConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'autoTest'
    verbose_name = u'自动化测试'
