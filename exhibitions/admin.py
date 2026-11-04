from django.contrib import admin
from .models import Artist, Project, ProjectImage


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "type", "location", "start_date", "end_date", "status")
    list_filter = ("type",)
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ProjectImageInline]


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}