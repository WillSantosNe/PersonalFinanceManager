from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from .models import Category, User
from .serializers import AdminCategorySerializer, CategorySerializer

class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling category CRUD operations.
    
    Access Rules:
    - Staff users can view, create, update, and delete any category.
    - Regular users can:
        - View all categories with limited information.
        - Create categories for themselves only.
        - Update and delete only their own categories.
    """

    permission_classes = [IsAuthenticated]


    def get_serializer(self, *args, **kwargs):
        """
        Ensure the request context is passed to the serializer.
        This helps in accessing user data inside the serializer.
        """
        kwargs["context"] = self.get_serializer_context()
        return super().get_serializer(*args, **kwargs)


    def get_serializer_class(self):
        """
        Selects the serializer based on user role:
        - Staff users get full control (AdminCategorySerializer).
        - Regular users get limited access (CategorySerializer).
        """
        return AdminCategorySerializer if self.request.user.is_staff else CategorySerializer


    def get_queryset(self):
        """
        Returns all categories.
        (Filtering is handled by serializer rules based on user role).
        """
        return Category.objects.all()


    def perform_create(self, serializer):
        """
        Handles category creation:
        - Staff users can assign categories to any user.
        - Regular users can only create categories for themselves.
        """
        user = self.request.user

        if "user" in self.request.data and not user.is_staff:
            raise PermissionDenied("Only staff members can create categories for others.")

        # Staff can assign to any user, regular users create for themselves
        serializer.save(user=user if not user.is_staff else serializer.validated_data.get('user', user))


    def perform_update(self, serializer):
        """
        Handles full updates (PUT):
        - Staff users can update any field for any category.
        - Regular users can only update 'name' and 'type' of their own categories.
        """
        instance = self.get_object()
        user = self.request.user

        if not user.is_staff:
            if instance.user != user:
                raise PermissionDenied("You can only update your own categories.")

            # Prevent non-staff users from modifying the 'user' field
            serializer.validated_data.pop("user", None)

        serializer.save()


    def partial_update(self, request, *args, **kwargs):
        """
        Handles partial updates (PATCH):
        - Staff users can partially update any field.
        - Regular users can only update 'name' and 'type' for their own categories.
        """
        instance = self.get_object()
        user = request.user

        if not user.is_staff:
            if instance.user != user:
                raise PermissionDenied("You can only update your own categories.")

            if "user" in request.data:
                raise PermissionDenied("You cannot change the category owner.")

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


    def perform_destroy(self, instance):
        """
        Handles category deletion:
        - Staff users can delete any category.
        - Regular users can only delete their own categories.
        """
        user = self.request.user
        if not user.is_staff and instance.user != user:
            raise PermissionDenied("You can only delete your own categories.")

        instance.delete()
