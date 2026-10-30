from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView
from .models import Exhibition

class ExhibitionList(ListView):
    model = Exhibition

class ExhibitionDetail(DetailView):
    model = Exhibition