from django.db import models
from django.contrib.auth import get_user_model
from categories.models import Category

User = get_user_model()

class Goal(models.Model):
    """
    Represents a financial goal set by a user, which can be associated with a specific category.

    Attributes:
        id (int): Unique identifier for the goal.
        user (User): The owner of the goal.
        category (Category, optional): The category associated with the goal.
        name (str): The name of the goal.
        target_amount (Decimal): The financial target to achieve.
        frequency (str): The frequency of the goal ('monthly' or 'yearly').
    """

    FREQUENCY_CHOICES = [
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name = 'goals',
        help_text="The user who owns this financial goal."
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='goals',
        help_text="The category related to this goal (optional)."
    )
    name = models.CharField(
        max_length=200,
        help_text="The name of the goal."
    )
    target_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="The financial target amount to achieve."
    )
    frequency = models.CharField(
        max_length=10,
        choices=FREQUENCY_CHOICES,
        help_text="The frequency of the goal: 'monthly' or 'yearly'."
    )

    class Meta:
        ordering = ['name']
        verbose_name = "Goal"
        verbose_name_plural = "Goals"

    def __str__(self):
        return f"{self.name} - Target: ${self.target_amount:.2f}"
