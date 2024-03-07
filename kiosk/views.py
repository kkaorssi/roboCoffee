from rest_framework import viewsets
from rest_framework.response import Response

from .serializers import RecipeSerializer

from .models import Recipe

# Create your views here.
    
class RecipeRouter(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    
    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        data = {"recipe": serializer.data}
        return Response(data)