from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from recipe.serializers import TagSerializer, IngredientSerializer
from core.models import Tag, Ingredient


class BaseRecipeAttrViewSet(viewsets.GenericViewSet, 
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin):
    """Base class for Tag and Ingredient viewsets in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')
    
    def perform_create(self, serializer):
        """Create a new tag"""
        serializer.save(user=self.request.user)


class TagViewSet(BaseRecipeAttrViewSet):
    """Manage tags in the database"""
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    

class IngredientViewSet(BaseRecipeAttrViewSet):
    """Manage views for the Ingredients model"""
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
