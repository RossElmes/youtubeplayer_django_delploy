from django.urls import path
from . import views

urlpatterns = [
    path('place-order/', views.place_order, name='place_order'),
    path('product-list/', views.product_list, name='product_list'),
    path('addproduct/', views.add_product, name='addproduct'),
    path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('add-to-order/<int:product_id>/', views.add_to_order, name='add_to_order'),
    path('order-detail/<int:order_id>/', views.order_detail, name='order_detail'),
    path('confirm-order/<int:order_id>/', views.confirm_order, name='confirm_order'),
    path('orderstoday/', views.orders_today, name='orders_today'),
]