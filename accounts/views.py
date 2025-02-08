from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import CustomUser
from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling user CRUD operations.
    Staff members can manage all users.
    Regular users can only update their own profiles.
    """

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Staff can see all users.
        Regular users can only see their own profile.
        """
        if self.request.user.is_staff:
            return CustomUser.objects.all()
        return CustomUser.objects.filter(id=self.request.user.id)

    def retrieve(self, request, *args, **kwargs):
        """
        Staff can view any profile.
        Regular users can only view their own profile.
        """
        instance = self.get_object()
        if not request.user.is_staff and instance != request.user:
            raise PermissionDenied("You can only view your own profile.")
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Staff can update any user.
        Regular users can only update their own profile.
        """
        instance = self.get_object()
        if not request.user.is_staff and instance != request.user:
            raise PermissionDenied("You can only update your own profile.")

        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        Staff can update any user.
        Regular users can only partially update their own profile.
        """
        instance = self.get_object()
        if not request.user.is_staff and instance != request.user:
            raise PermissionDenied("You can only update your own profile.")

        return super().partial_update(request, *args, **kwargs)

    def perform_destroy(self, instance):
        """
        Only staff members can delete users.
        Regular users cannot delete any account, including their own.
        """
        if not self.request.user.is_staff:
            raise PermissionDenied("Only staff members can delete users.")
        
        instance.delete()
