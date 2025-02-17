from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    """Model to store additional user details (Optional)"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - Profile"


class Expense(models.Model):
    """Model to store user expenses"""

    CATEGORY_CHOICES = [
        ('Food', 'Food'),
        ('Travel', 'Travel'),
        ('Rent', 'Rent'),
        ('Shopping', 'Shopping'),
        ('Utilities', 'Utilities'),
        ('Entertainment', 'Entertainment'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="expenses", db_index=True)  # ✅ Indexed Foreign Key
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, db_index=True)  # ✅ Indexing improves filtering speed
    description = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True, db_index=True)  # ✅ Index for faster date filtering
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)  # ✅ Tracks record creation
    updated_at = models.DateTimeField(auto_now=True, db_index=True)  # ✅ Tracks last update

    def __str__(self):
        return f"{self.user.username} - {self.category} - ${self.amount} ({self.date})"

    class Meta:
        ordering = ["-date"]  # ✅ Ensures recent expenses appear first
        indexes = [
            models.Index(fields=["date"]),  # ✅ Explicit index for date-based queries
            models.Index(fields=["category"]),  # ✅ Explicit index for category-based filtering
            models.Index(fields=["user", "date"]),  # ✅ Optimized index for filtering user expenses by date
        ]
