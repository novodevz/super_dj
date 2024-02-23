from rest_framework import serializers  # qs


class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        # model = Model
        fields = "__all__"


# register serializer import
from django.contrib.auth.models import User


# register serializer class
class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


from .models import Category, Department, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "department",
            "category",
            "slug",
        ]


class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)  # Serialize nested Product objects

    class Meta:
        model = Category
        fields = ["id", "name", "description", "slug", "products"]


class DepartmentSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)  # Serialize nested Product objects

    class Meta:
        model = Department
        fields = ["id", "name", "description", "slug", "products"]
