from django.db import models
from django.contrib.auth.models import User
import uuid


# Create your models here.

# TODO: Refactor Income and Expense into Transaction Model to prevent repeated code.


class Income(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    date = models.DateTimeField()
    category = models.TextField()
    notes = models.TextField()
    labels = models.TextField(blank=True, null=True)
    is_monthly_recurring = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.TextField()
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return (
            f"{self.amount}, {self.date}, {self.category}, {self.notes}, {self.labels}"
        )


class Expense(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    date = models.DateTimeField()
    category = models.TextField()
    notes = models.TextField()
    labels = models.TextField(blank=True, null=True)
    is_monthly_recurring = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.TextField()
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.amount}, {self.date}, {self.category}, {self.notes}, {self.id}"


class Category(models.Model):
    class TransactionType(models.TextChoices):
        # Actual value ↓      # ↓ Displayed on Django Admin
        INCOME = "INCOME", "Income"
        EXPENSE = "EXPENSE", "Expense"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.TextField()
    transaction_type = models.TextField(
        choices=(
            ("INCOME", "Income"),
            ("EXPENSE", "Expense"),
        ),
        default="EXPENSE",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.type
