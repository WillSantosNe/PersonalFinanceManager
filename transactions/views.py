from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Transaction
from .serializers import TransactionSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Staff members can see all transactions.
        Regular users can only see their own transactions.
        """
        user = self.request.user

        if user.is_staff:
            return Transaction.objects.all()
        
        return Transaction.objects.filter(user=user)
    

    def perform_create(self, serializer):
        """                                                                                                       
        Automatically assign the logged-in user to the transaction.
        """
        serializer.save(user=self.request.user)


    def perform_update(self, serializer):
        """
        Allow only staff or the owner to update transactions.
        """
        instance = self.get_object()
        if not self.request.user.is_staff and instance.user != self.request.user:
            raise PermissionDenied("You can only update your own transactions.")
        serializer.save()


    def perform_destroy(self, instance):
        """
        Allow only staff or the owner to delete transactions.
        """
        if not self.request.user.is_staff and instance.user != self.request.user:
            raise PermissionDenied("You can only delete your own transactions.")
        instance.delete()
