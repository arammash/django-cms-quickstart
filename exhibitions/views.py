from django.views.generic import ListView, DetailView
from .models import Project

class ExhibitionList(ListView):
    queryset = Project.objects.filter(type=Project.Type.EXHIBITION)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        projects = list(context["object_list"])

        context["future_projects"] = [p for p in projects if p.status == "future"]
        context["current_projects"] = [p for p in projects if p.status == "current"]
        context["past_projects"] = [p for p in projects if p.status == "past"]
        return context

class ExhibitionDetail(DetailView):
    queryset = Project.objects.filter(type=Project.Type.EXHIBITION)