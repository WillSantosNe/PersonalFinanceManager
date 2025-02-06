from django.db import models
from django.contrib.auth import get_user_model
from categories.models import Category

User = get_user_model()

class Transaction(models.Model):
    """
    Represents a financial transaction, either an income or an expense.

    Attributes:
        id (int): Unique identifier for the transaction.
        user (User): The owner of the transaction.
        category (Category): The category associated with the transaction.
        type (str): Type of transaction ('income' or 'expense').
        date (date): The date when the transaction occurred.
        amount (Decimal): The monetary value of the transaction.
        description (str, optional): Additional details about the transaction.
    """

    TYPE_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]

    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='transactions',
        help_text="The user who owns this transaction."
    )
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE,
        related_name='transactions',
        help_text="The category associated with this transaction."
    )
    type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        help_text="Type of transaction: 'income' for earnings, 'expense' for spending."
    )
    date = models.DateField(
        help_text="The date when the transaction occurred."
    )
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="The amount of money involved in this transaction."
    )
    description = models.TextField(
        blank=True, 
        null=True,
        help_text="Additional details or notes about the transaction."
    )

    class Meta:
        ordering = ['-date']
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"

    def __str__(self):
        return f"{self.type.capitalize()} - ${self.amount:.2f}"
