from django.apps import AppConfig


class K8SdeployConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'k8sDeploy'
    verbose_name = u'集群部署'
