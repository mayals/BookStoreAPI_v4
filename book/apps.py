from django.apps import AppConfig


class BookConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'book'

     # Note: signal NOT work without this code :
    def ready(self):
        import book.signals