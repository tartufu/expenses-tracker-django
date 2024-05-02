from rest_framework import serializers
from .models import Expense, Income


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = [
            "id",
            "amount",
            "date",
            "category",
            "notes",
            "labels",
            "is_monthly_recurring",
            "type",
        ]


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = [
            "id",
            "amount",
            "date",
            "category",
            "notes",
            "labels",
            "is_monthly_recurring",
            "type",
        ]


def serializeData(serializerType, model):
    serializer = serializerType(model)
    serialized_data = serializer.data
    return serialized_data
