from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Income(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    is_monthly_recurrring = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
