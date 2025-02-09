from datetime import datetime
from django.db.models import Sum
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from transactions.models import Transaction
from .serializers import DashboardSerializer

class DashboardViewSet(viewsets.ViewSet):
    """
    ViewSet for retrieving user financial statistics.
    """
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """
        Returns financial statistics for the authenticated user.
        """
        user = request.user
        current_month = datetime.now().month
        current_year = datetime.now().year

        # Calculate total income and expenses for the current month
        total_income = Transaction.objects.filter(
            user=user, type="income", date__month=current_month, date__year=current_year
        ).aggregate(total=Sum("amount"))["total"] or 0

        total_expense = Transaction.objects.filter(
            user=user, type="expense", date__month=current_month, date__year=current_year
        ).aggregate(total=Sum("amount"))["total"] or 0

        # Balance calculation
        balance = total_income - total_expense

        # Find the category with the highest expense
        highest_expense_category = (
            Transaction.objects.filter(user=user, type="expense", date__month=current_month, date__year=current_year)
            .values("category__name")
            .annotate(total_spent=Sum("amount"))
            .order_by("-total_spent")
            .first()
        )

        data = {
            "total_income": total_income,
            "total_expense": total_expense,
            "balance": balance,
            "highest_expense_category": highest_expense_category["category__name"] if highest_expense_category else None,
            "highest_expense_amount": highest_expense_category["total_spent"] if highest_expense_category else 0,
        }

        serializer = DashboardSerializer(data)
        return Response(serializer.data)
