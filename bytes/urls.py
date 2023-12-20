from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('accounts/signup/', views.signup, name='signup'),
    path('bytes/', views.product_list, name='product_list'),
    path('bytes/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    # path("create-checkout-session/<int:pk>/",views.create_checkout_session, name="create-checkout-session"),
    path("create-checkout-session/<int:pk>/",views.CreateStripeCheckoutSessionView.as_view(),  name="create-checkout-session"),
    path("success/", views.SuccessView.as_view(), name="success"),
    path("cancel/", views.CancelView.as_view(), name="cancel"),

    # path('bytes/', views.bytes_index, name='index'),
    # path('bytes/<int:byte_id>/', views.bytes_detail, name='detail'),
    # path('cart/', views.cart, name='cart'),
    # path('cart/<int:byte_id>/add/', views.cart_add, name='cart_add'),
    # path('cart/<int:order_detail_id>/delete', views.item_delete, name='item_delete'),
    # path('cart/checkout', views.cart_checkout, name='cart_checkout'),
    # path('cart/<int:order_detail_id>/update', views.item_update, name='item_update'),
    # path('orders/', views.orders, name='orders'),
    # path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    # path("create-checkout-session/<int:pk>/",    CreateStripeCheckoutSessionView.as_view(),        name="create-checkout-session"),
]


