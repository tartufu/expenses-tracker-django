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

from .models import Income


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
    return Response({"message": "Hello, world!"})


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

    amount = request.data["amount"]
    user = User.objects.get(username=user)

    print(request.data["amount"])
    income_record = Income.objects.create(user_id=user, amount=amount)
    return Response(
        {
            "success": True,
            "data": {"amount": amount},
        }
    )
