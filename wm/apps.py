from django.apps import AppConfig

class WMConfig(AppConfig):
    name = 'wm'
    verbose_name = 'Warehouse Management'

    def ready(self):
        import wm.signals
