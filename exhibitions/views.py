from django.views.generic import ListView, DetailView
from .models import Project
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