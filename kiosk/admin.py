from django.contrib import admin

from .models import Recipe
from .models import Bookmark
from .models import Order

# Register your models here.
admin.site.register(Recipe)
admin.site.register(Bookmark)
admin.site.register(Order)
