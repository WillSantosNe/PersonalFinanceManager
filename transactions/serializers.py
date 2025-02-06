from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for the Transaction model.
    Defines how transaction data is serialized/deserialized in the API.
    """

    class Meta:
        model = Transaction
        fields = ['id', 'user', 'category', 'type', 'date', 'amount', 'description']
