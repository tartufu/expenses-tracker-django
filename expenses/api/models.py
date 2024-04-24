from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Income(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    is_monthly_recurrring = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Transaction(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    category = models.TextField()
    notes = models.TextField()
    is_monthly_recurrring = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Category(models.Model):
    class TransactionType(models.TextChoices):
        # Actual value ↓      # ↓ Displayed on Django Admin
        INCOME = "INCOME", "Income"
        EXPENSE = "EXPENSE", "Expense"

    type = models.TextField()
    transaction_type = models.TextField(
        choices=(
            ("INCOME", "Income"),
            ("EXPENSE", "Expense"),
        ),
        default="EXPENSE",
    )

    def __str__(self):
        return self.type
