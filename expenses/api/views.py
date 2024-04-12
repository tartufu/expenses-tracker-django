from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.core.management.utils import get_random_secret_key
from dotenv import load_dotenv
import os


@api_view(["GET"])
def hello_world(request):
    load_dotenv()
    print(get_random_secret_key())
    print(os.getenv("SECRET_KEY"))
    return Response({"message": "Hello, world!"})
