from django.views.generic import ListView, DetailView
from .models import Project

class ExhibitionList(ListView):
    queryset = Project.objects.filter(type=Project.Type.EXHIBITION)

class ExhibitionDetail(DetailView):
    queryset = Project.objects.filter(type=Project.Type.EXHIBITION)