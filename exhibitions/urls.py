from django.urls import path
from . import views

app_name = 'exhibitions'
urlpatterns = [
    path('', views.ExhibitionList.as_view(), name='exhibition_list'),
    path('<slug:slug>/', views.ExhibitionDetail.as_view(), name='exhibition_detail'),
]