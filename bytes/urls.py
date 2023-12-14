from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('bytes/', views.bytes_index, name='index'),
    path('bytes/<int:byte_id>/', views.bytes_detail, name='detail')
]