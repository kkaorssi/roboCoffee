from django.urls import include, path
from rest_framework import routers

from kiosk.views import RecipeRouter, BookmarkRouter, OrderRouter
from kiosk import views

router = routers.DefaultRouter()
router.register(r'recipe', RecipeRouter)
router.register(r'bookmark', BookmarkRouter)
router.register(r'order', OrderRouter)

urlpatterns = [
    path('', include(router.urls)),
]