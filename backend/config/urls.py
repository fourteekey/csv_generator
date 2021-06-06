from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(openapi.Info(title="CsvGenerator API", default_version='v1'), url=settings.API_URL)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/v1/', include('api.api', namespace='api_urls')),

    path('admin/', admin.site.urls),
    path('', include('csv_generator.urls'), name='index')

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
