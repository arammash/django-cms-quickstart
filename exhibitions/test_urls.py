from django.urls import include, path

urlpatterns = [
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
