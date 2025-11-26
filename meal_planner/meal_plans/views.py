from django.shortcuts import render

def home(request):
    """The home page for Meal Plans."""
    return render(request, 'meal_plans/home.html')
