from django.db import models
from django.contrib.auth.models import AbstractUser


class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE, related_name="car_models")
    dealer_id = models.IntegerField()
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50, choices=[("Sedan", "Sedan"), ("SUV", "SUV"), ("Wagon", "Wagon")])
    year = models.DateField()

    def __str__(self):
        return f"{self.car_make.name} {self.name}"
