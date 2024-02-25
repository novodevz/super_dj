import os

from base.serializers import RegistrationSerializer
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import status

# Create your views here.
from rest_framework.decorators import api_view  # qs
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response  # qs
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView


@api_view(["GET"])
@permission_classes([AllowAny])
def index(request):
    response = "home"
    return Response(response)


# i’m protected
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def secret(req):
    return Response("secret")


@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    serializer = RegistrationSerializer(data=request.data)

    if serializer.is_valid():
        username = serializer.validated_data["username"]

        # Check if the user with the provided username already exists
        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "Username is already taken."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create a new user
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        response_data = {
            "username": user.username,
            "access_token": access_token,
        }

        return Response(response_data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["username"] = user.username
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


from base.models import Category, Department, Product
from base.serializers import CategorySerializer, DepartmentSerializer, ProductSerializer
from django.contrib.auth.decorators import user_passes_test


# Define a custom function to check if the user is an admin
def user_is_admin(user):
    return user.is_authenticated and user.is_superuser


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
# @user_passes_test(user_is_admin)
def get_all_deps_prods(request):
    # Query all departments along with their related products
    departments = Department.objects.prefetch_related("products").all()
    # Serialize the data
    department_serializer = DepartmentSerializer(departments, many=True)
    # Return the serialized data as a JSON response
    return Response(department_serializer.data)


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
# @user_passes_test(user_is_admin)
def get_all_cats_prods(request):
    categories = Category.objects.prefetch_related("products").all()
    category_serializer = CategorySerializer(categories, many=True)
    return Response(category_serializer.data)


@api_view(["GET"])
def get_dep_prods(request, dep_slug):
    try:
        # Query the department by slug
        department = Department.objects.prefetch_related("products").get(slug=dep_slug)
    except Department.DoesNotExist:
        return Response(
            {"error": "Department not found."}, status=status.HTTP_404_NOT_FOUND
        )

    # Serialize the department along with its products
    department_serializer = DepartmentSerializer(department)
    return Response(department_serializer.data)


@api_view(["GET"])
def get_cat_prods(request, cat_slug):
    try:
        # Query the category by slug
        category = Category.objects.prefetch_related("products").get(slug=cat_slug)
    except Category.DoesNotExist:
        return Response(
            {"error": "Category not found."}, status=status.HTTP_404_NOT_FOUND
        )

    # Serialize the category along with its products
    category_serializer = CategorySerializer(category)
    return Response(category_serializer.data)


@api_view(["GET"])
def get_prods_by_dep_cat(request, dep_slug, cat_slug):
    try:
        # Retrieve products based on department and category slugs
        products = Product.objects.filter(
            department__slug=dep_slug,
            category__slug=cat_slug,  # Using double underscores to traverse relationships between models for filtering
        )
        # Serialize the data
        serializer = ProductSerializer(products, many=True)
        # Return the serialized data as a JSON response
        return Response(serializer.data)
    except Product.DoesNotExist:
        # Handle the case where no products are found for the given slugs
        return Response(
            {
                "error": "No products found for the specified department and category slugs"
            },
            status=status.HTTP_404_NOT_FOUND,
        )


import random
import string

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from PIL import Image


def random_string(length):
    characters = string.ascii_lowercase + string.digits
    return "".join(random.choice(characters) for _ in range(length))


def generate_unique_filename(original_filename, k):
    # Generate a random string of 4 characters
    random_chars = "".join(random.choices(string.ascii_letters + string.digits, k=k))

    # Split the original filename and get the file extension
    filename, extension = os.path.splitext(original_filename)

    # Combine the random string with the original filename and extension
    unique_filename = f"{filename}_{random_chars}{extension}"

    return unique_filename


# fake_request_files = {
#     "image": {
#         "filename": "example.jpg",
#         "content_type": "image/jpeg",
#         "content": b"fake_image_content",  # Bytes representing the image content
#     },
#     "document": {
#         "filename": "example.pdf",
#         "content_type": "application/pdf",
#         "content": b"fake_document_content",  # Bytes representing the document content
#     }
# }


from django.db import IntegrityError


@api_view(["POST"])
def add_prod(request):
    if request.method == "POST":
        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            product_name = serializer.validated_data.get("name")

            # Check if a product with the same name already exists
            if Product.objects.filter(name=product_name).exists():
                return Response(
                    {"error": "Product with the same name already exists."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            print(request.FILES)
            # Handle image upload
            if "imageFile" in request.FILES:
                image_file = request.FILES["imageFile"]

                # Generate a unique filename
                unique_filename = generate_unique_filename(image_file.name, 5)

                try:
                    # Save the image using default storage
                    image_path = default_storage.save(unique_filename, image_file)

                    # Save the product instance with the image field
                    serializer.save(image=image_path)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                except IntegrityError as e:
                    # Handle database integrity error
                    return Response(
                        {"error": "Product with the same name already exists."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                except Exception as e:
                    # Handle other potential errors
                    print("An error occurred:", e)
                    return Response(
                        {"error": "An error occurred while saving the product."},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )

            else:
                # If no image is provided, save the product instance without the image field
                try:
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                except Exception as e:
                    # Handle other potential errors
                    print("An error occurred:", e)
                    return Response(
                        {"error": "An error occurred while saving the product."},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response(
            {"error": "Invalid request method"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )
