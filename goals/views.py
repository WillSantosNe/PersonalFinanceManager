from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Goal
from .serializers import GoalSerializer

class GoalViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling goal CRUD operations.
    Users can only manage their own goals.
    Staff members can access all goals.
    """
    
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Staff can see all goals.
        Regular users can only see their own goals.
        """
        user = self.request.user
        if user.is_staff:
            return Goal.objects.all()
        return Goal.objects.filter(user=user)

    def perform_create(self, serializer):
        """
        Automatically assign the logged-in user to the goal.
        """
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        """
        Ensure that only the owner can update their own goals.
        """
        instance = self.get_object()
        if not self.request.user.is_staff and instance.user != self.request.user:
            raise PermissionDenied("You can only update your own goals.")
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        """
        Ensure that only the owner can partially update their own goals.
        """
        instance = self.get_object()
        if not request.user.is_staff and instance.user != request.user:
            raise PermissionDenied("You can only update your own goals.")
        return super().partial_update(request, *args, **kwargs)

    def perform_destroy(self, instance):
        """
        Ensure that only the owner can delete their own goals.
        Staff members can delete any goal.
        """
        if not self.request.user.is_staff and instance.user != self.request.user:
            raise PermissionDenied("You can only delete your own goals.")
        
        instance.delete()
