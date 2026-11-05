from django.contrib import admin
from django.http import HttpResponse
from .models import Artist, Project, ProjectImage


class CloseToolbarModalOnSaveMixin:
    def response_add(self, request, obj, post_url_continue=None):
        response = super().response_add(request, obj, post_url_continue)
        if self._should_close_toolbar_modal(request, response):
            return self._close_toolbar_modal_response()
        return response

    def response_change(self, request, obj):
        response = super().response_change(request, obj)
        if self._should_close_toolbar_modal(request, response):
            return self._close_toolbar_modal_response()
        return response

    def _should_close_toolbar_modal(self, request, response):
        return (
            request.GET.get("cms_modal") == "1"
            and response.status_code in (302, 303)
            and not {"_continue", "_addanother", "_saveasnew"}.intersection(request.POST)
        )

    @staticmethod
    def _close_toolbar_modal_response():
        return HttpResponse(
            """<!doctype html>
<html><body>
<script>
  window.parent.document
    .querySelector(".cms-modal-close, .frontend-edit-dialog [data-close-frontend-editor]")
    ?.click();
</script>
</body></html>"""
        )


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1


@admin.register(Project)
class ProjectAdmin(CloseToolbarModalOnSaveMixin, admin.ModelAdmin):
    list_display = ("title", "type", "location", "start_date", "end_date", "status")
    list_filter = ("type",)
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ProjectImageInline]


@admin.register(Artist)
class ArtistAdmin(CloseToolbarModalOnSaveMixin, admin.ModelAdmin):
    list_display = ("name", "slug", "is_core_artist")
    list_display_links = ("name",)
    list_filter = ("is_core_artist",)
    prepopulated_fields = {"slug": ("name",)}