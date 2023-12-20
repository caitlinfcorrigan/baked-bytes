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
    path('cart/<int:order_detail_id>/delete', views.item_delete, name='item_delete'),
    path('cart/checkout', views.cart_checkout, name='cart_checkout'),
    path('cart/<int:order_detail_id>/update', views.item_update, name='item_update'),
    path('orders/', views.orders, name='orders'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    # path('orders/<int:order_id>/', views.OrderDetail.as_view(), name="orders_detail"),

    path("create-payment-intent", views.createpayment, name="create-payment-intent"),
    path("payment-complete", views.paymentcomplete, name="payment-complete"),

]


