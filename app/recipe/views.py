from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from recipe.serializers import TagSerializer
from core.models import Tag


class TagViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Manage tags in the database"""
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')
