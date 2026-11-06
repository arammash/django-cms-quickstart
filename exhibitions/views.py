from django.views.generic import ListView, DetailView
from .models import Artist, Project
from django.shortcuts import get_object_or_404, render

def render_project_detail(request, id):
    obj = get_object_or_404(Project, id=id)
    request.toolbar.set_object(obj)
    return render(
        request,
        "exhibitions/project_detail.html",
        {
            "object": obj,
        }
    )

class ExhibitionList(ListView):
    queryset = Project.objects.filter(type=Project.Type.EXHIBITION)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        projects = list(context["object_list"])

        context["current_projects"] = [p for p in projects if p.status == "current"]
        context["past_projects"] = [p for p in projects if p.status == "past"]
        context["future_projects"] = [p for p in projects if p.status == "future"]
        return context

class ExhibitionDetail(DetailView):
    queryset = Project.objects.filter(type=Project.Type.EXHIBITION)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.request.toolbar.set_object(self.object)
        return context


class ArtistList(ListView):
    model = Artist
    template_name = "exhibitions/artist_list.html"
    context_object_name = "artists"

    def get_queryset(self):
        return Artist.objects.filter(is_core_artist=True)


class ArtistDetail(DetailView):
    model = Artist
    template_name = "exhibitions/artist_detail.html"
    context_object_name = "artist"

    def get_queryset(self):
        return Artist.objects.filter(is_core_artist=True).prefetch_related(
            "project_set__images",
            "project_set__artists",
            "gallery_images__image",
            "external_links",
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["projects"] = self.object.project_set.all()
        context["external_links"] = self.object.external_links.all()

        carousel_images = []
        if self.object.hero_image:
            carousel_images.append(
                {
                    "url": self.object.hero_image.url,
                    "alt": self.object.hero_image.default_alt_text or self.object.name,
                    "caption": self.object.hero_image.default_caption,
                }
            )
        carousel_images.extend(
            {
                "url": gallery_image.image.url,
                "alt": gallery_image.title or self.object.name,
                "caption": gallery_image.caption,
            }
            for gallery_image in self.object.gallery_images.all()
        )
        context["carousel_images"] = carousel_images
        return context