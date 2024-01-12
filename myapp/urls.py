from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('checkout', views.checkout, name='checkout'),
    path('receipt/<int:receipt_id>', views.receipt, name='receipt'),
    path('profile', views.profile, name='profile'),
    path('desktops', views.desktops, name='Desktops'),
    path('laptops', views.laptops, name='Laptops'),
    path('monitors', views.monitors, name='Monitors'),
    path('keyboards', views.keyboards, name='Keyboards'),
    path('mice', views.mice, name='Mice'),
    path('headsets', views.headsets, name='Headsets'),
    path('chairs', views.chairs, name='Chairs'),
    path('bags/', views.bags, name='bags'),
    path('cart', views.cart, name='cart')
    ]