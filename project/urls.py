from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
# https://drf-yasg.readthedocs.io/en/stable/readme.html#usage
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="BookStoreAPI",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('user.urls')),  # user application url
    path('books/', include('book.urls')),  # book application url
    path('ecommerces/', include('ecommerce.urls')),
    # path('api-auth/', include('rest_framework.urls')), not need 
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# swagger
# https://drf-yasg.readthedocs.io/en/stable/readme.html#usage
urlpatterns +=[
   path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]