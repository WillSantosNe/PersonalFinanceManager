from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()  # Get the custom user model

class Category(models.Model):
    """
    Model representing a category.

    Attributes:
        user (User): The user to whom the category belongs.
        name (str): The name of the category.
        type (str): The type of category, chosen from the TYPE_CHOICES.
    """

    TYPE_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
        ('mixed', 'Mixed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Each category belongs to a user
    name = models.CharField(max_length=100)  # Name of the category
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)  # Type of the category (Enum)

    class Meta:
        """
        Meta options for the Category model.

        Attributes:
            unique_together (tuple): Ensures that each user can have unique category names.
        """
        unique_together = ('user', 'name')  # Each user can have unique category names

    def __str__(self):
        return self.name
