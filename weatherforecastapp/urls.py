from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePage, name='home_page'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('add_city/', views.AddCity, name = 'add_city'),
    path('city/<str:city_name>', views.city, name = 'city_weather_forecast'),
    path('city', views.city, name = 'city_weather_forecast'),
    path('delete_city/<str:city_name>', views.deleteCity, name = 'delete_city'),
    path('delete_user/', views.deleteUser, name = 'delete_user'),
    path('message/', views.message, name = 'message'),
]