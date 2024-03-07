from django.urls import include, path
from rest_framework import routers

from kiosk.views import RecipeRouter

router = routers.DefaultRouter()
router.register(r'recipe', RecipeRouter)

urlpatterns = [
    path('', include(router.urls)),
]