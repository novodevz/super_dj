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
