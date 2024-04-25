from django.urls import path
from . import views

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("hello-world/", views.hello_world, name="hello_world"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("sign-up/", views.sign_up, name="sign_up"),
    path("sign-in/", views.sign_in, name="sign_in"),
    path(
        "get-user-details/<str:user>/", views.get_user_details, name="get_user_details"
    ),
    path("<str:user>/add-income", views.add_user_income, name="add_user_income"),
    path("<str:user>/get-income", views.get_user_income, name="get_user_income"),
    path("<str:user>/add-expense", views.add_user_expense, name="add_user_expense"),
    path("<str:user>/get-expense", views.get_user_expense, name="get_user_expense"),
    path(
        "get-transaction-types",
        views.get_transaction_types,
        name="get_transaction_types",
    ),
]

# https://medium.com/django-unleashed/securing-django-rest-apis-with-jwt-authentication-using-simple-jwt-a-step-by-step-guide-28efa84666fe
