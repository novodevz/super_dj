# base urls.py

from base import views
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

# fmt: off
urlpatterns = [
    path("", views.index, name="app_index"),
    path("secret/", views.secret, name="app_secret"),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('register/', views.register, name='register'),
    path('login/', views.MyTokenObtainPairView.as_view(), name='token'),
    path('db/all/departments/products/', views.get_all_deps_prods, name='base-get_all_deps_prods'), # is_user_admin implemented
    path('db/all/categories/products/', views.get_all_cats_prods, name='base-get_all_cats_prods'), # is_user_admin implemented
    path('department/<str:dep_slug>', views.get_dep_prods, name='base-get_dep_prods'),
    path('category/<str:cat_slug>', views.get_cat_prods, name='base-get_cat_prods'),
    path('department/<str:dep_slug>/category/<str:cat_slug>', views.get_prods_by_dep_cat, name='base-get_prods_by_dep_cat'),
    path('add_prod', views.add_prod, name='base-add_prod'),
    path('get_dep_cat_info', views.get_dep_cat_info, name='base-get_dep_cat_info')
]
