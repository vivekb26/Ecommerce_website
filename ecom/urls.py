from django.urls import path,include
from .views import ProductListView
from . import views
urlpatterns = [
    path('',views.home, name="ecom-home"),
    # path('',ProductListView.as_view(), name="ecom-home"),
    path('cart/',views.cart, name="cart"),
    path('checkout/',views.checkout, name="checkout"),
    path('product_detail/<int:pk>/',views.product_detail, name="product_detail"),
    path('update_item/',views.updateItem, name="update_item"),
    path('process_order/',views.processOrder, name="process_order"),
]