from django.urls import path
from . import views

urlpatterns = [
    path("hello-world/", views.hello_world, name="hello_world"),
    path("sign-up/", views.sign_up, name="sign_up"),
]
