"""
URL configuration for ask_pavlovskii project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('',view=views.index,name='index'),
    path('auth/register', views.register, name='register'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('sales-cards/', views.sales_cards, name='sales_cards'),
    path('delete-profile/', views.delete_profile, name='delete_profile'),
    path('help/', views.help, name='help'),
    path('favorites/', views.favorites, name='favorites'),
    path('lists/', views.list_view, name='list_view'),
    path('lists/<int:id>/edit/', views.list_edit, name='list_edit'),
    path('product/<int:id>/', views.product_info, name='product_info'),
    path('cart/add/', views.add_to_cart, name='add_to_cart'),
    path('cart/view/', views.cart_view_partial, name='cart_view'),
    path('cart/increase/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/', views.decrease_quantity, name='decrease_quantity'),
]
