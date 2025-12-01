from django.shortcuts import render

from .models import Pizza

def index(request):
    return render(request, 'pizzerias/index.html')

def pizzas(request):
    """Show all Pizzas"""
    pizzas = Pizza.objects.order_by('date_added')
    context = {'pizzas':pizzas}
    return render(request, 'pizzerias/pizzas.html', context)

def pizza(request, pizza_id):
    """Show a single Pizza and all its toppings"""
    pizza = Pizza.objects.get(id=pizza_id)
    toppings = pizza.topping_set.order_by('-date_added')
    context = {'pizza': pizza, 'toppings': toppings}
    return render(request, 'pizzerias/pizza.html', context)