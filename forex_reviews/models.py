from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Company(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField(max_length=255, unique=True)

class Review(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField(default=0, 
                                 validators=[
                                     MaxValueValidator(5),
                                     MinValueValidator(0)
                                 ]
                                 )
    date = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=255)
    