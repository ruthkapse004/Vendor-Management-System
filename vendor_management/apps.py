from django.apps import AppConfig


class VendorManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vendor_management'

    def ready(self) -> None:
        import vendor_management.signals
