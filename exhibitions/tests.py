from django.conf import settings
from django.test import TestCase
from django.test import override_settings
from django.urls import reverse

from filer.models import Image as FilerImage

from .models import Artist, ArtistExternalLink, ArtistImage, Project, ProjectImage


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
        self.assertContains(response, "Exhibition Only")

    def test_artist_directory_lists_past_exhibitions_and_non_core_artists(self):
        past_exhibition = Project.objects.create(
            title="Past Exhibition",
            slug="past-exhibition",
            start_date="2000-01-01",
            end_date="2000-02-01",
        )
        past_exhibition.artists.add(self.artist, self.exhibition_only_artist)
        Project.objects.create(
            title="Future Exhibition",
            slug="future-exhibition",
            start_date="2999-01-01",
        )
        other_artist = Artist.objects.create(name="Another Other Artist", slug="another-other")

        response = self.client.get(reverse("artists:artist_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Past Exhibition")
        self.assertContains(response, "Exhibition Only")
        self.assertContains(response, "Another Other Artist")
        self.assertContains(response, f'data-artist-id="{self.artist.pk}"', html=False)
        self.assertContains(response, 'aria-label="Clear exhibition selection"', html=False)
        self.assertContains(response, ">clear</button>", html=False)
        rendered = response.content.decode()
        self.assertLess(
            rendered.index(f'data-artist-id="{self.artist.pk}"'),
            rendered.index(f'data-artist-id="{self.exhibition_only_artist.pk}"'),
        )
        self.assertNotContains(response, "Future Exhibition")
        self.assertNotContains(response, 'href="/artists/exhibition-only/"')
        self.assertContains(
            response,
            f'data-artist-ids="{self.artist.pk},{self.exhibition_only_artist.pk}"',
            html=False,
        )
        self.assertContains(
            response,
            f'data-artist-id="{self.exhibition_only_artist.pk}"',
            html=False,
        )

    def test_artist_detail_displays_artist_name(self):
        response = self.client.get(self.artist.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Alex Artist")

    def test_artist_detail_exposes_admin_edit_area_in_frontend_edit_mode(self):
        from django.contrib.auth import get_user_model

        user = get_user_model().objects.create_superuser(
            username="artist-editor",
            email="artist-editor@example.com",
            password="test-password",
        )
        self.client.force_login(user)

        response = self.client.get(f"{self.artist.get_absolute_url()}?edit=on")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-frontend-edit-url="/admin/exhibitions/artist/')
        self.assertContains(response, "Double-click to edit this artist")

    def test_artist_profile_sections_and_external_links_render(self):
        self.artist.bio = "A short artist biography."
        self.artist.website_url = "https://artist.example.com/"
        self.artist.instagram_url = "https://instagram.com/artist"
        self.artist.cv_url = "https://artist.example.com/cv"
        self.artist.save()
        solo = Project.objects.create(
            title="Solo Exhibition",
            slug="solo-exhibition",
            start_date="2025-01-01",
        )
        solo.artists.add(self.artist)
        group = Project.objects.create(
            title="Group Exhibition",
            slug="group-exhibition",
            start_date="2024-01-01",
        )
        group.artists.add(self.artist, self.exhibition_only_artist)
        ArtistExternalLink.objects.create(
            artist=self.artist,
            title="Interview",
            url="https://example.com/interview",
        )

        response = self.client.get(self.artist.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        for content in (
            "A short artist biography.",
            "Website",
            "Instagram",
            "Exhibitions",
            "CV",
            "Explore",
            "Solo Exhibition",
            "Group Exhibition",
            "Interview",
        ):
            self.assertContains(response, content)
        self.assertNotContains(response, "Solo exhibitions")
        self.assertNotContains(response, "Group exhibitions")
        self.assertNotContains(response, 'href="#biography"', html=False)
        self.assertNotContains(response, 'href="#exhibitions"', html=False)
        self.assertNotContains(response, 'href="#cv"', html=False)
        self.assertNotContains(response, 'href="#explore"', html=False)
        self.assertEqual(response.content.decode().count('id="exhibitions"'), 1)

    def test_artist_carousel_starts_with_hero_image(self):
        hero = FilerImage.objects.create(
            name="Hero image",
            original_filename="hero.jpg",
            file="artists/hero.jpg",
            mime_type="image/jpeg",
        )
        gallery = FilerImage.objects.create(
            name="Gallery image",
            original_filename="gallery.jpg",
            file="artists/gallery.jpg",
            mime_type="image/jpeg",
        )
        self.artist.hero_image = hero
        self.artist.save()
        ArtistImage.objects.create(
            artist=self.artist,
            image=gallery,
            caption="Gallery caption",
        )

        response = self.client.get(self.artist.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertRegex(
            response.content.decode(),
            r'<figure class="image-carousel__slide is-active">\s*<img[^>]+/media/artists/hero\.jpg',
        )
        self.assertContains(response, "/media/artists/gallery.jpg")

    def test_exhibition_only_artist_has_no_public_artist_page(self):
        response = self.client.get(self.exhibition_only_artist.get_absolute_url())

        self.assertEqual(response.status_code, 404)


@override_settings(
    ROOT_URLCONF="exhibitions.test_urls",
    STORAGES={
        **settings.STORAGES,
        "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
    }
)
class ExhibitionGalleryTests(TestCase):
    def test_exhibition_list_shows_titles_and_date_ranges_without_locations(self):
        Project.objects.create(
            title="Upcoming Exhibition",
            slug="upcoming-exhibition",
            location="Hidden Gallery",
            start_date="2027-01-02",
            end_date="2027-01-05",
        )
        Project.objects.create(
            title="New Year Exhibition",
            slug="new-year-exhibition",
            start_date="2027-12-29",
            end_date="2028-01-03",
        )

        response = self.client.get(reverse("exhibitions:exhibition_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Upcoming Exhibition")
        self.assertContains(response, "02/01 - 05/01/27")
        self.assertContains(response, "29/12/27 - 03/01/28")
        self.assertNotContains(response, "Hidden Gallery")
        self.assertRegex(
            response.content.decode(),
            r'<a href="/testing/upcoming-exhibition/">Upcoming Exhibition</a><br>\s*<span class="project-dates">\s*02/01 - 05/01/27',
        )

    def test_exhibition_images_render_as_captioned_carousel(self):
        project = Project.objects.create(
            title="Gallery Exhibition",
            slug="gallery-exhibition",
            start_date="2026-01-01",
        )
        for index, caption in enumerate(("First caption", "Second caption"), start=1):
            image = FilerImage.objects.create(
                name=f"Gallery image {index}",
                original_filename=f"gallery-{index}.jpg",
                file=f"gallery/gallery-{index}.jpg",
                mime_type="image/jpeg",
            )
            ProjectImage.objects.create(
                project=project,
                image=image,
                caption=caption,
                order=index,
            )

        response = self.client.get(project.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-image-carousel')
        self.assertContains(response, 'data-carousel-previous')
        self.assertContains(response, 'data-carousel-next')
        self.assertContains(response, "First caption")
        self.assertContains(response, "Second caption")
        self.assertContains(response, 'src="/media/gallery/gallery-1.jpg"')
        self.assertRegex(
            response.content.decode(),
            r'<figure[^>]*hidden[^>]*>\s*<img[^>]+gallery-2\.jpg',
        )


@override_settings(
    STORAGES={
        **settings.STORAGES,
        "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
    }
)
class ArtistGalleryAdminTests(TestCase):
    def setUp(self):
        from django.contrib.auth import get_user_model

        user = get_user_model().objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="password",
        )
        self.client.force_login(user)
        self.artist = Artist.objects.create(name="Gallery Artist", slug="gallery-artist")

    def test_artist_edit_form_includes_gallery_image_caption_fields(self):
        response = self.client.get(
            reverse("admin:exhibitions_artist_change", args=[self.artist.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Caption / description")
        self.assertContains(response, "gallery_images-TOTAL_FORMS")
        self.assertContains(response, "external_links-TOTAL_FORMS")


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
            {
                "name": "Modal Artist",
                "slug": "modal-artist",
                "gallery_images-TOTAL_FORMS": "0",
                "gallery_images-INITIAL_FORMS": "0",
                "external_links-TOTAL_FORMS": "0",
                "external_links-INITIAL_FORMS": "0",
                "_save": "Save",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(".cms-modal-close", response.content.decode())
        self.assertTrue(Artist.objects.filter(slug="modal-artist").exists())

    def test_artist_admin_list_name_links_to_edit_form(self):
        artist = Artist.objects.create(name="Linked Artist", slug="linked-artist")

        response = self.client.get(reverse("admin:exhibitions_artist_changelist"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            f'href="{reverse("admin:exhibitions_artist_change", args=[artist.pk])}"',
        )

    def test_save_and_continue_keeps_artist_form_open(self):
        response = self.client.post(
            f"{reverse('admin:exhibitions_artist_add')}?cms_modal=1",
            {
                "name": "Continuing Artist",
                "slug": "continuing-artist",
                "gallery_images-TOTAL_FORMS": "0",
                "gallery_images-INITIAL_FORMS": "0",
                "external_links-TOTAL_FORMS": "0",
                "external_links-INITIAL_FORMS": "0",
                "_continue": "Save",
            },
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
            {
                "name": "First Artist",
                "slug": "first-artist",
                "gallery_images-TOTAL_FORMS": "0",
                "gallery_images-INITIAL_FORMS": "0",
                "external_links-TOTAL_FORMS": "0",
                "external_links-INITIAL_FORMS": "0",
                "_addanother": "Save",
            },
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
