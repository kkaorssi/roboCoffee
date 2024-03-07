from django.db import models

# Create your models here.
class Recipe(models.Model):
    bean_name = models.CharField(max_length=200)
    pattern = models.CharField(max_length=200)
    water = models.IntegerField(default=0)
    bean_weight = models.IntegerField(default=0)
    rinsing = models.BooleanField(default=True)
    drip = models.IntegerField(default=0)
    mode = models.CharField(max_length=200, default='Parameter')
    
    def __str__(self):
        return self.recipe_name