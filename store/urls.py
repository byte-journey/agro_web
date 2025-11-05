from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/<slug:slug>/', views.category_view, name='category-view'),
    path('shop/', views.shop, name='shop'),
    path('product/<int:pk>/', views.product_detail, name='product-detail'),
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name="add_to_cart"),    
    path('wishlist/', views.wishlist, name="wishlist"),
    path('update-cart/<int:item_id>/', views.update_cart_item, name='update_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order-confirmation'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('search/', views.search, name='search'),
    path('contact/', views.contact, name='contact'),
    # Auth
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),

    path('api/product/<int:pk>/', views.product_api, name="product-api"),
]