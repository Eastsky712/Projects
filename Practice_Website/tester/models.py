from django.db import models

class Beginning(models.Model):
    text = models.TextField(max_length=50)
    class Number(models.IntegerChoices):
        POOR = 1, 'Poor'
        AVERAGE = 2, 'Average'
        GOOD = 3, 'Good'
        EXCELLENT = 4, 'Excellent'

    number = models.IntegerField(choices=Number.choices)

    def __str__(self):
        return f"Review ID {self.pk} - {self.get_number_display()}"

class Middle(models.Model):
    text = models.TextField(max_length=50)

    def __str__(self):
        return self.text


class Last(models.Model):
    text = models.TextField(max_length=50)

    def __str__(self):
        return self.text
