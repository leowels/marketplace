# marketplace_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
     # Главная страница
    path('', views.home, name='home'),

    # Регистрация и авторизация
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Профили
    path('profile/', views.profile, name='profile'),
    path('client_profile/', views.client_profile, name='client_profile'),
    path('master_profile/', views.master_profile, name='master_profile'),

    # Регистрация клиентов и мастеров
    path('register_client/', views.register_client, name='register_client'),
    path('register_master/', views.register_master, name='register_master'),

    # Просмотр мастера и создание заказа
    path('master/<int:master_id>/', views.view_master, name='view_master'),
    path('create_order/<int:master_id>/', views.create_order, name='create_order'),

    # Оставить отзыв
    path('master/<int:master_id>/leave_review/', views.leave_review, name='leave_review'),

    # Список продуктов
    path('product_list/', views.product_list, name='product_list'),
    
    # Добавление продукта
    path('add_product/', views.add_product, name='add_product'),
]
