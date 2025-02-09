from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Report(models.Model):
    """
    Model to store generated financial reports.
    """
    FORMAT_CHOICES = [
        ('pdf', 'PDF'),
        ('excel', 'Excel'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE) # User
    format = models.CharField(max_length=10, choices=FORMAT_CHOICES) # PDF or Excel
    created_at = models.DateTimeField(auto_now_add=True) # Auto-generated timestamp
    file = models.FileField(upload_to='reports/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.format.upper()} Report ({self.created_at})"
