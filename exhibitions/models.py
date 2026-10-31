from django.db import models
from django.urls import reverse
from filer.fields.image import FilerImageField

class Artist(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

class Project(models.Model):
    class Type(models.TextChoices):
        EXHIBITION = "exhibition", "Exhibition"
        # later, add e.g. RESIDENCY = "residency", "Residency"

    type = models.CharField(max_length=30, choices=Type.choices, default=Type.EXHIBITION)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    artists = models.ManyToManyField(Artist, blank=True)
    text = models.TextField(blank=True)

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("exhibitions:exhibition_detail", kwargs={"slug": self.slug})


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, related_name="images", on_delete=models.CASCADE)
    image = FilerImageField(on_delete=models.PROTECT)
    caption = models.CharField(max_length=300, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]