"""Defines URL patterns for pizzeria."""

from django.urls import path

from . import views

app_name = 'pizzerias'
urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    # Page that shows all Pizzas
    path('pizzas/', views.pizzas, name='pizzas'),
    # Detailed page for single Pizza
    path('pizzas/<int:pizza_id>/', views.pizza, name='pizza'),
]