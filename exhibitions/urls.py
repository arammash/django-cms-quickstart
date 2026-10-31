from django.urls import path
from . import views

from exhibitions import views
from . import views

app_name = 'exhibitions'
urlpatterns = [
     path('', views.ExhibitionList.as_view(), name='exhibition_list'),
    path('<slug:slug>/', views.ExhibitionDetail.as_view(), name='exhibition_detail'),
]