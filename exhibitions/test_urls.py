from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "artists/",
        include(("exhibitions.artist_urls", "artists"), namespace="artists"),
    ),
    path(
        "testing/",
        include(("exhibitions.urls", "exhibitions"), namespace="exhibitions"),
    ),
    path("", include("cms.urls")),
]
