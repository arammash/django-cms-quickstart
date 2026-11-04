from django.conf import settings
from django.test import TestCase
from django.test import override_settings
from django.urls import reverse

from .models import Artist


@override_settings(
    ROOT_URLCONF="exhibitions.test_urls",
    STORAGES={
        **settings.STORAGES,
        "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
    }
)
class ArtistPageTests(TestCase):
    def setUp(self):
        self.artist = Artist.objects.create(name="Alex Artist", slug="alex-artist")

    def test_artist_directory_links_to_artist_detail(self):
        response = self.client.get(reverse("artists:artist_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Alex Artist")
        self.assertContains(response, reverse("artists:artist_detail", kwargs={"slug": "alex-artist"}))

    def test_artist_detail_displays_artist_name(self):
        response = self.client.get(self.artist.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Alex Artist")
