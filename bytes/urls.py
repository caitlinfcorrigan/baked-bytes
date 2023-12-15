from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('bytes/', views.bytes_index, name='index'),
    path('bytes/<int:byte_id>/', views.bytes_detail, name='detail'),
    path('accounts/signup/', views.signup, name='signup'),
    path('cart/', views.cart, name='cart'),
    path('cart/<int:byte_id>/add/', views.cart_add, name='cart_add'),
    # path('cart/<int:byte_id>/delete', views.CartDelete.as_view(), name='byte_delete'),
    # path('cart/<int:byte_id>/update', views.CartUpdate, name='byte_update')
]

