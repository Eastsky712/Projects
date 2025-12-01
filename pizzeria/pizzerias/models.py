from django.db import models

class Pizza(models.Model):
    """A Pizza the user has inputted"""
    name = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Topping(models.Model):
    """A specific topping on the pizza"""
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'toppings'

    def __str__(self):
        return self.name