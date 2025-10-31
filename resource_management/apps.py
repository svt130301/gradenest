from django.apps import AppConfig
class ResourceManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'resource_management'

    def ready(self):
        # Import signals so they are registered automatically
        import resource_management.signals  # noqa

