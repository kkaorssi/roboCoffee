from django.db import models

# Create your models here.
class Recipe(models.Model):
    coffee_beans = models.CharField(max_length=200)
    drip_method = models.CharField(max_length=200)
    ground_amount = models.IntegerField(default=0)
    brewing_ratio = models.IntegerField(default=0)
    total_amount = models.IntegerField(default=0)
    
    def __str__(self):
        return str(self.id)
    
class Bookmark(models.Model):
    recipe_name = models.CharField(max_length=200)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.recipe_name

class Order(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    drip_pos = models.IntegerField(default=0)
    state = models.CharField(max_length=200)
    order_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.id)
    
    class Meta:
        ordering = ['order_time']