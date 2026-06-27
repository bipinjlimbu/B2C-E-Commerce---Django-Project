from django.urls import path
from .views.auth_view import register_view, login_view, logout_view
from .views.main_view import home_view
from .views.profile_view import profile_view, edit_profile_view, delete_profile_view
from .views.brand_view import add_brand_view, edit_brand_view, delete_brand_view
from .views.product_view import products_view, add_product_view, edit_product_view, is_active_toggle_view, delete_product_view, single_product_view
from .views.cart_view import add_to_cart_view, cart_view, increase_cart_item_quantity, decrease_cart_item_quantity, remove_cart_item
from .views.wishlist_view import wishlist_view, wishlist_toggle_view, wishlist_remove_view
from .views.payment_view import initiate_esewa_payment
from .views.dashboard import admin_dashboard_view, customer_dashboard_view

urlpatterns = [
    path('', home_view, name='home'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', edit_profile_view, name='edit_profile'),
    path('profile/delete/<int:user_id>/', delete_profile_view, name='delete_profile'),
    path('brands/add/', add_brand_view, name='add_brand'),
    path('brands/edit/<int:brand_id>/', edit_brand_view, name='edit_brand'),
    path('brands/delete/<int:brand_id>/', delete_brand_view, name='delete_brand'),
    path('products/', products_view, name='products'),
    path('products/add/', add_product_view, name='add_product'),
    path('products/edit/<int:product_id>/', edit_product_view, name='edit_product'),
    path('products/toggle-status/<int:product_id>/', is_active_toggle_view, name='toggle_product_active'),
    path('products/delete/<int:product_id>/', delete_product_view, name='delete_product'),
    path('products/<int:product_id>/', single_product_view, name='single_product'),
    path('cart/add/<int:product_id>/', add_to_cart_view, name='add_to_cart'),
    path('cart/', cart_view, name='cart'),
    path('cart/increase/<int:product_id>/', increase_cart_item_quantity, name='increase_cart_item_quantity'),
    path('cart/decrease/<int:product_id>/', decrease_cart_item_quantity, name='decrease_cart_item_quantity'),
    path('cart/remove/<int:product_id>/', remove_cart_item, name='remove_cart_item'),
    path('wishlist/', wishlist_view, name='wishlist'),
    path('products/wishlist-toggle/<int:product_id>/', wishlist_toggle_view, name='wishlist_toggle'), 
    path('products/wishlist/remove/<int:product_id>/', wishlist_remove_view, name='wishlist_remove'),  
    path('payment/initiate/', initiate_esewa_payment, name='initiate_esewa_payment'),
    path('dashboard/admin/', admin_dashboard_view, name='admin_dashboard'),
    path('dashboard/', customer_dashboard_view, name='customer_dashboard'),
]