from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.product_list, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('products/<slug:slug>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_detail, name='cart'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:item_id>/', views.cart_remove, name='cart_remove'),
    path('cart/update/<int:item_id>/', views.cart_update, name='cart_update'),
    path('checkout/', views.checkout, name='checkout'),
    path('order/<int:pk>/confirm/', views.order_confirm, name='order_confirm'),
    path('orders/', views.order_history, name='order_history'),
    path('accounts/register/', views.register, name='register'),
]
