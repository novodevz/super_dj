# base urls.py

from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from base import views

# fmt: off
urlpatterns = [
    path("", views.index, name="app_index"),
    path("secret/", views.secret, name="app_secret"),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('register/', views.register, name='register'),
    path('login/', views.MyTokenObtainPairView.as_view(), name='token'),
]
