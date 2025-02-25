from rest_framework import serializers
from .models import Category, User

class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for regular users.

    - Allows users to create categories only for themselves.
    - Prevents manual assignment of the 'user' field.
    - Limits exposed user data to email, first_name, and last_name.
    """

    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,
        default=serializers.CurrentUserDefault()  # Automatically assigns the logged-in user
    )

    class Meta:
        model = Category
        fields = ["name", "type", "user"]


    def create(self, validated_data):
        """
        Handles the creation of a category.
        Automatically assigns the logged-in user if not explicitly provided.
        """
        return super().create(validated_data)


    def validate(self, attrs):
        """
        Validates input data to ensure regular users cannot assign
        categories to other users.

        Raises:
            serializers.ValidationError: If the 'user' field is manually set.
        """
        # Block attempts to assign categories to other users
        if "user" in self.initial_data:
            raise serializers.ValidationError({
                "user": "You cannot assign categories to other users."
            })

        # Remove user from attributes to avoid conflicts
        attrs.pop("user", None)
        return attrs


    def to_representation(self, instance):
        """
        Customizes the output representation for regular users.

        Exposes limited user details:
        - email
        - first_name
        - last_name
        """
        data = super().to_representation(instance)
        data["user"] = {
            "email": instance.user.email,
            "first_name": instance.user.first_name,
            "last_name": instance.user.last_name
        }
        return data


class AdminCategorySerializer(serializers.ModelSerializer):
    """
    Serializer for staff users.

    - Grants full control over all categories.
    - Allows assignment of categories to any user.
    - Provides detailed user information in responses.
    """

    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,
        default=serializers.CurrentUserDefault()  # Automatically assigns the logged-in user if not provided
    )

    class Meta:
        model = Category
        fields = ["id", "name", "type", "user"]


    def validate(self, attrs):
        """
        Validates the data for staff users.

        - If 'user' is not provided, assigns the logged-in user.
        """
        request = self.context.get("request")
        if "user" not in attrs:
            attrs["user"] = request.user
        return attrs


    def to_representation(self, instance):
        """
        Customizes the output representation for staff users.

        Exposes detailed user information:
        - id
        - email
        - first_name
        - last_name
        - is_active
        - is_staff
        """
        data = super().to_representation(instance)
        if hasattr(instance, "user"):
            data["user"] = {
                "id": instance.user.id,
                "email": instance.user.email,
                "first_name": instance.user.first_name,
                "last_name": instance.user.last_name,
                "is_active": instance.user.is_active,
                "is_staff": instance.user.is_staff
            }
        return data
