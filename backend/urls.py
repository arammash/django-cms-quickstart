from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.apps import apps

urlpatterns = [
    path('admin/', admin.site.urls),

    # Django CMS URLs catch-all at root
    path('', include('cms.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Disable the new Django admin sidebar for better UX with Django CMS custom admin views
admin.site.enable_nav_sidebar = False
