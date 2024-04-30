from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone


from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.forms.models import model_to_dict


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
        user_id=user, created_at__month=current_month, is_deleted=False
    ).values("amount")
    user_income_sum = 0

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
    type = request.data["type"]
    user = User.objects.get(username=user)

    income_record = Income.objects.create(
        user_id=user,
        category=category,
        notes=notes,
        labels=label,
        date=date,
        amount=amount,
        type=type,
    )

    return Response(
        {
            "success": True,
            "data": model_to_dict(income_record),
        }
    )


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def edit_user_income(request, user):

    id, type, category, date, amount, notes, labels, is_monthly = (
        request.data["id"],
        request.data["type"],
        request.data["category"],
        request.data["date"]["startDate"],
        request.data["amount"],
        request.data["notes"],
        request.data["label"],
        request.data["isMonthly"],
    )
    print(request.data["id"])
    print(request.data)

    user_income = Income.objects.get(id=id)

    print(user_income)

    user_income.type = type
    user_income.category = category
    user_income.date = date
    user_income.amount = amount
    user_income.notes = notes
    user_income.labels = labels
    user_income.is_monthly = is_monthly

    user_income.save()

    return Response(
        {
            "success": True,
            "data": {"user_income": model_to_dict(user_income)},
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
    type = request.data["type"]

    user = User.objects.get(username=user)

    expense_record = Expense.objects.create(
        user_id=user,
        category=category,
        notes=notes,
        labels=label,
        date=date,
        amount=amount,
        type=type,
    )
    print(expense_record)

    return Response({"success": True, "data": model_to_dict(expense_record)})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_expense(request, user):

    user = User.objects.get(username=user)

    current_month = timezone.now().month

    user_expense_list = Expense.objects.filter(
        user_id=user, created_at__month=current_month, is_deleted=False
    ).values("amount")
    user_expense_sum = 0

    print(user_expense_list)

    for expense in user_expense_list:
        user_expense_sum += expense["amount"]

    print(user_expense_sum)

    return Response(
        {
            "success": True,
            "data": {"amount": user_expense_sum},
        }
    )


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def edit_user_expense(request, user):

    id, type, category, date, amount, notes, labels, is_monthly = (
        request.data["id"],
        request.data["type"],
        request.data["category"],
        request.data["date"]["startDate"],
        request.data["amount"],
        request.data["notes"],
        request.data["label"],
        request.data["isMonthly"],
    )
    print(request.data["id"])
    print(request.data)

    user_expense = Expense.objects.get(id=id)

    print(user_expense)

    user_expense.type = type
    user_expense.category = category
    user_expense.date = date
    user_expense.amount = amount
    user_expense.notes = notes
    user_expense.labels = labels
    user_expense.is_monthly = is_monthly

    user_expense.save()

    return Response(
        {
            "success": True,
            "data": {"user_expense": model_to_dict(user_expense)},
        }
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def delete_user_transaction(request, user):

    id, type = (request.data["id"], request.data["type"])

    record = None

    if type == "Expense":
        record = Expense.objects.get(id=request.data["id"])
    if type == "Income":
        record = Income.objects.get(id=request.data["id"])

    record.is_deleted = True
    record.save()

    return Response(
        {
            "success": True,
            "data": {"id": record.id},
        }
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def get_all_user_transaction(request, user):

    # print(user_expense_sum)

    user = User.objects.get(username="chang")

    current_month = timezone.now().month

    user_expense_list = Expense.objects.filter(
        user_id=user, created_at__month=current_month, is_deleted=False
    ).values()

    user_income_list = Income.objects.filter(
        user_id=user, created_at__month=current_month, is_deleted=False
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
