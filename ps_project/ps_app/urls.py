from django.urls import path
from .views.auth_view import register_view, login_view, logout_view
from .views.main_view import home_view
from .views.profile_view import profile_view, edit_profile_view, delete_profile_view
from .views.brand_view import add_brand_view
from .views.dashboard import admin_dashboard_view

urlpatterns = [
    path('', home_view, name='home'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', edit_profile_view, name='edit_profile'),
    path('profile/delete/', delete_profile_view, name='delete_profile'),
    path('brands/add/', add_brand_view, name='add_brand'),
    path('dashboard/admin/', admin_dashboard_view, name='admin_dashboard'),
]