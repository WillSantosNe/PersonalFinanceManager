from rest_framework import serializers

class DashboardSerializer(serializers.Serializer):
    """
    Serializer for the user financial dashboard statistics.
    """
    total_income = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_expense = serializers.DecimalField(max_digits=10, decimal_places=2)
    balance = serializers.DecimalField(max_digits=10, decimal_places=2)
    highest_expense_category = serializers.CharField(allow_null=True)
    highest_expense_amount = serializers.DecimalField(max_digits=10, decimal_places=2, allow_null=True)
