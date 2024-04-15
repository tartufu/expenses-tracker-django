from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.contrib.auth.models import User
from django.db.models import Q


@api_view(["GET", "POST"])
def hello_world(request):
    return Response({"message": "Hello, world!"})


@api_view(["POST"])
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

    user = User.objects.create_user(
        username=request.data["username"],
        email=request.data["email"],
        password=request.data["password"],
    )
    # TODO return auth token, username and email
    return Response({"message": "Hello, user!"})
