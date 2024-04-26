from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone


from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from django.db.models import Q

from .models import Income, Category, Expense


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def hello_world(request):
    return Response({"message": "Hello, world!"})


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


@api_view(["POST"])
@permission_classes([AllowAny])
def sign_up(request):
    username, email, password = (
        request.data["username"],
        request.data["email"],
        request.data["password"],
    )

    print(username, email, password)

    try:
        user = User.objects.filter(Q(username=username) | Q(email=email))
        if user.exists():
            raise ValueError("Username/Email already exists!")

    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=400)

    user = User.objects.create_user(username=username, email=email, password=password)

    token = get_tokens_for_user(user)

    return Response(
        {
            "success": True,
            "data": {
                "access": token["access"],
                "refresh": token["refresh"],
                "username": username,
                "email": email,
            },
        }
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def sign_in(request):
    username, password = (
        request.data["username"],
        request.data["password"],
    )

    user = authenticate(username=username, password=password)

    if user is not None:
        token = get_tokens_for_user(user)
        return Response(
            {
                "success": True,
                "data": {
                    "access": token["access"],
                    "refresh": token["refresh"],
                    "username": username,
                    "email": user.email,
                },
            }
        )
    else:
        return Response(
            {
                "success": False,
                "errorMsg": "Invalid User or Password Details!",
            }
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_details(request, user):
    print(user)
    user = User.objects.get(id=user)
    print(213123)
    print(user.email)
    return Response(
        {
            "success": True,
            "data": {"email": user.email, "username": user.username},
        }
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_income(request, user):

    user = User.objects.get(username=user)

    current_month = timezone.now().month

    user_income_list = Income.objects.filter(
        user_id=user, created_at__month=current_month
    ).values("amount")
    user_income_sum = 0

    print(user_income_list)

    for income in user_income_list:
        user_income_sum += income["amount"]

    print(user_income_sum)
    return Response(
        {
            "success": True,
            "data": {"amount": user_income_sum},
        }
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_user_income(request, user):

    category = request.data["category"]
    date = request.data["date"]["startDate"]
    amount = request.data["amount"]
    notes = request.data["notes"]
    label = request.data["label"]
    user = User.objects.get(username=user)

    income_record = Income.objects.create(
        user_id=user,
        category=category,
        notes=notes,
        labels=label,
        date=date,
        amount=amount,
    )

    print(income_record)
    return Response(
        {
            "success": True,
            "data": {"amount": amount},
        }
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_user_expense(request, user):

    # const postBody = { type, category, date, amount, notes, label };

    category = request.data["category"]
    date = request.data["date"]["startDate"]
    amount = request.data["amount"]
    notes = request.data["notes"]
    label = request.data["label"]
    user = User.objects.get(username=user)

    expense_record = Expense.objects.create(
        user_id=user,
        category=category,
        notes=notes,
        labels=label,
        date=date,
        amount=amount,
    )
    print(expense_record)

    return Response(
        {
            "success": True,
            "data": {"amount": 5555},
        }
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_expense(request, user):

    user = User.objects.get(username=user)

    current_month = timezone.now().month

    user_expense_list = Expense.objects.filter(
        user_id=user, created_at__month=current_month
    ).values("amount")
    user_expense_sum = 0

    print(user_expense_list)

    for expense in user_expense_list:
        user_expense_sum += expense["amount"]

    print(user_expense_sum)

    # print(user_expense_sum)
    return Response(
        {
            "success": True,
            "data": {"amount": user_expense_sum},
        }
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def get_user_transaction(request, user):

    # print(user_expense_sum)

    user = User.objects.get(username="chang")

    current_month = timezone.now().month

    user_expense_list = Expense.objects.filter(
        user_id=user, created_at__month=current_month
    ).values()

    user_income_list = Income.objects.filter(
        user_id=user, created_at__month=current_month
    ).values()

    merged_list = user_expense_list.union(user_income_list).order_by("-date")

    return Response({"success": True, "data": merged_list})


@api_view(["GET"])
@permission_classes([AllowAny])
def get_transaction_types(request):

    transaction_types = Category.objects.all()
    transaction_types_list = list(transaction_types.values())

    return Response(
        {
            "success": True,
            "data": transaction_types_list,
        }
    )
