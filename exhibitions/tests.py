from django.conf import settings
from django.test import TestCase
from django.test import override_settings
from django.urls import reverse

from .models import Artist, Project


@override_settings(
    ROOT_URLCONF="exhibitions.test_urls",
    STORAGES={
        **settings.STORAGES,
        "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
    }
)
class ArtistPageTests(TestCase):
    def setUp(self):
        self.artist = Artist.objects.create(
            name="Alex Artist",
            slug="alex-artist",
            is_core_artist=True,
        )
        self.exhibition_only_artist = Artist.objects.create(
            name="Exhibition Only",
            slug="exhibition-only",
        )

    def test_artist_directory_only_shows_core_artists(self):
        response = self.client.get(reverse("artists:artist_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Alex Artist")
        self.assertContains(response, reverse("artists:artist_detail", kwargs={"slug": "alex-artist"}))
        self.assertNotContains(response, "Exhibition Only")

    def test_artist_detail_displays_artist_name(self):
        response = self.client.get(self.artist.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Alex Artist")

    def test_exhibition_only_artist_has_no_public_artist_page(self):
        response = self.client.get(self.exhibition_only_artist.get_absolute_url())

        self.assertEqual(response.status_code, 404)


@override_settings(
    STORAGES={
        **settings.STORAGES,
        "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
    }
)
class ToolbarModalSaveTests(TestCase):
    def setUp(self):
        from django.contrib.auth import get_user_model

        user = get_user_model().objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="password",
        )
        self.client.force_login(user)

    def test_saving_artist_from_toolbar_modal_closes_modal(self):
        response = self.client.post(
            f"{reverse('admin:exhibitions_artist_add')}?cms_modal=1",
            {"name": "Modal Artist", "slug": "modal-artist", "_save": "Save"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(".cms-modal-close", response.content.decode())
        self.assertTrue(Artist.objects.filter(slug="modal-artist").exists())

    def test_save_and_continue_keeps_artist_form_open(self):
        response = self.client.post(
            f"{reverse('admin:exhibitions_artist_add')}?cms_modal=1",
            {"name": "Continuing Artist", "slug": "continuing-artist", "_continue": "Save"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertNotIn(".cms-modal-close", response.get("Location", ""))
        self.assertIn(
            reverse("admin:exhibitions_artist_change", args=[Artist.objects.get(slug="continuing-artist").pk]),
            response["Location"],
        )

    def test_save_and_add_another_keeps_artist_form_open(self):
        response = self.client.post(
            f"{reverse('admin:exhibitions_artist_add')}?cms_modal=1",
            {"name": "First Artist", "slug": "first-artist", "_addanother": "Save"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("admin:exhibitions_artist_add"), response["Location"])
        self.assertNotIn(".cms-modal-close", response.get("Location", ""))

    def test_saving_project_from_toolbar_modal_closes_modal(self):
        response = self.client.post(
            f"{reverse('admin:exhibitions_project_add')}?cms_modal=1",
            {
                "title": "Modal Project",
                "slug": "modal-project",
                "type": Project.Type.EXHIBITION,
                "start_date": "2026-01-01",
                "images-TOTAL_FORMS": "0",
                "images-INITIAL_FORMS": "0",
                "_save": "Save",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(".cms-modal-close", response.content.decode())
        self.assertTrue(Project.objects.filter(slug="modal-project").exists())

    def test_saving_project_edit_closes_frontend_edit_dialog(self):
        project = Project.objects.create(
            title="Editable Project",
            slug="editable-project",
            start_date="2026-01-01",
        )

        response = self.client.post(
            f"{reverse('admin:exhibitions_project_change', args=[project.pk])}?cms_modal=1",
            {
                "title": "Updated Project",
                "slug": "editable-project",
                "type": Project.Type.EXHIBITION,
                "start_date": "2026-01-01",
                "images-TOTAL_FORMS": "0",
                "images-INITIAL_FORMS": "0",
                "_save": "Save",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(".frontend-edit-dialog", response.content.decode())
        self.assertTrue(Project.objects.filter(pk=project.pk, title="Updated Project").exists())
