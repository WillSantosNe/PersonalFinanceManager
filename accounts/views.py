from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import CustomUser
from .serializers import AdminUserSerializer, UserSerializer, ChangePasswordSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling user CRUD operations.
    Staff members can manage all users.
    Regular users can only update their own profiles.
    """
    permission_classes = [IsAuthenticated]

    def get_serializer(self, *args, **kwargs):
        """
        Ensure request context is passed to the serializer.
        """
        kwargs["context"] = self.get_serializer_context()
        return super().get_serializer(*args, **kwargs)
    


    def get_serializer_class(self):
        """
        Use different serializers for admins and regular users.
        """
        if self.request.user.is_staff:
            return AdminUserSerializer
        return UserSerializer


    def get_queryset(self):
        """
        - Admins (`is_staff=True`) can see all users completely.
        - Common users (`is_staff=False`) can see all users, but only with the fields from the `UserSerializer`.
        """
        return CustomUser.objects.all()



    def retrieve(self, request, *args, **kwargs):
        """
        - Admins can see all details.
        - Common users can see any user, but only the permitted fields.
        """
        instance = self.get_object()
        return super().retrieve(request, *args, **kwargs)

    

    def update(self, request, *args, **kwargs):
        """
        Allow users to update only their own profile.
        Prevents users from updating password via this endpoint.
        """
        instance = self.get_object()
        if not request.user.is_staff and instance != request.user:
            raise PermissionDenied("You can only update your own profile.")

        serializer = self.get_serializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True) # um print funciona somente acima daqui
        serializer.save()

        
        return Response(serializer.data)
    

    def partial_update(self, request, *args, **kwargs):
        """
        Allow partial updates but prevent password changes here.
        """
        instance = self.get_object()
        if not request.user.is_staff and instance != request.user:
            raise PermissionDenied("You can only update your own profile.")

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data)
    

    def perform_destroy(self, instance):
        """
        Only staff members can delete users.
        Regular users cannot delete any account, including their own.
        """
        if not self.request.user.is_staff:
            raise PermissionDenied("Only staff members can delete other users.")

        if instance == self.request.user:
            raise PermissionDenied("You cannot delete your own account.")

        instance.delete()
        

    @action(detail=True, methods=["post"], url_path="change-password")
    def change_password(self, request, pk=None):
        """
        Allow a user to change their own password.
        """
        instance = self.get_object()
        if instance != request.user:
            raise PermissionDenied("You can only change your own password.")

        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.update(instance, serializer.validated_data)

        return Response({"detail": "Password updated successfully"}, status=status.HTTP_200_OK)
