from django.db import models
from django.urls import reverse
from django.utils import timezone
from cms.models.fields import PlaceholderRelationField
from filer.fields.image import FilerImageField
from cms.models.pluginmodel import CMSPlugin

class Artist(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    is_core_artist = models.BooleanField(
        "Core artist",
        default=False,
        help_text="Show this artist in the public Artists section.",
    )
    bio = models.TextField("Biography", blank=True)
    website_url = models.URLField("Website", blank=True)
    instagram_url = models.URLField("Instagram", blank=True)
    cv_url = models.URLField("CV link", blank=True)
    cv_file = models.FileField("CV PDF", upload_to="artist-cvs/", blank=True)
    hero_image = FilerImageField(
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="artist_hero_images",
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("artists:artist_detail", kwargs={"slug": self.slug})


class ArtistExternalLink(models.Model):
    artist = models.ForeignKey(Artist, related_name="external_links", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    url = models.URLField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "pk"]

    def __str__(self):
        return f"{self.artist}: {self.title}"


class ArtistImage(models.Model):
    artist = models.ForeignKey(Artist, related_name="gallery_images", on_delete=models.CASCADE)
    image = FilerImageField(on_delete=models.PROTECT)
    title = models.CharField(max_length=200, blank=True)
    caption = models.TextField("Caption / description", blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "pk"]

    def __str__(self):
        return self.title or f"{self.artist} image {self.order + 1}"


class Project(models.Model):
    class Type(models.TextChoices):
        EXHIBITION = "exhibition", "Exhibition"
        # later, add e.g. RESIDENCY = "residency", "Residency"

    type = models.CharField(max_length=30, choices=Type.choices, default=Type.EXHIBITION)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    location = models.CharField(max_length=200, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    artists = models.ManyToManyField(Artist, blank=True)
    text = models.TextField(blank=True)
    placeholders = PlaceholderRelationField()

    def get_template(self):
        return "exhibitions/project_detail.html"

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return self.title

    @property
    def status(self):
        if self.start_date > timezone.localdate():
            return "future"
        if self.end_date is None or self.end_date >= timezone.localdate():
            return "current"
        return "past"

    def get_absolute_url(self):
        return reverse("exhibitions:exhibition_detail", kwargs={"slug": self.slug})


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, related_name="images", on_delete=models.CASCADE)
    image = FilerImageField(on_delete=models.PROTECT)
    caption = models.CharField(max_length=300, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

class ProjectPluginModel(CMSPlugin):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="plugins")

    def __str__(self):
        return f"Project Plugin: {self.project.title}"