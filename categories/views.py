from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Category
from .serializers import CategorySerializer

class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling category CRUD operations.
    Users can only access their own categories.
    """
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Ensure users only see their own categories.
        """
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """                                                                                                       
        Automatically assign the logged-in user to the category.
        """
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        """
        Allow users to update only their own categories.
        """
        instance = self.get_object()
        if not self.request.user.is_staff and instance.user != self.request.user:
            raise PermissionDenied("You can only update your own categories.")
        
        serializer.save()

    def perform_destroy(self, instance):
        """
        Allow users to delete only their own categories.
        Only staff can delete any category.
        """
        if not self.request.user.is_staff and instance.user != self.request.user:
            raise PermissionDenied("You can only delete your own categories.")

        instance.delete()
