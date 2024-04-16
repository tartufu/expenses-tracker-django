from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from django.db.models import Q


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
