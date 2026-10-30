from django.db import models

# Create your models here.
from filer.fields.image import FilerImageField

class Artist(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Exhibition(models.Model):
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

class ExhibitionImage(models.Model):
    exhibition = models.ForeignKey(Exhibition, related_name="images", on_delete=models.CASCADE)
    image = FilerImageField(on_delete=models.PROTECT)
    caption = models.CharField(max_length=300, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
