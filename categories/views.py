from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Category
from .serializers import CategorySerializer

class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling category CRUD operations.
    Users can only access their own categories.
    Staff members can manage all categories.
    """
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Staff can see all categories.
        Regular users can only see their own categories.
        """
        if self.request.user.is_staff:
            return Category.objects.all()
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Automatically assign the logged-in user to the category.
        """
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        """
        Allow users to update only their own categories.
        Only staff can update any category.
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
            raise PermissionDenied("You can only delete your own categories. Only staff can delete any category.")

        instance.delete()
