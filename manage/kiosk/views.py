from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from .serializers import RecipeSerializer, BookmarkSerializer, OrderSerializer

from .models import Recipe, Bookmark, Order

# Create your views here.
class RecipeRouter(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    
    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        data = {"recipe": serializer.data}
        return Response(data)
    
class BookmarkRouter(viewsets.ModelViewSet):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    
    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        data = {"bookmark": serializer.data}
        return Response(data)
    
class OrderRouter(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        data = {"order": serializer.data}
        return Response(data)