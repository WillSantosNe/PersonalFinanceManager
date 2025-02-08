from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser
from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling user CRUD operations.
    Only authenticated users can access.
    """

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Ensure that users can only access their own profile.
        """
        return CustomUser.objects.filter(id=self.request.user.id)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
