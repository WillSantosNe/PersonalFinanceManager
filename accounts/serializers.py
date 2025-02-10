from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for regular users. Staff can see all details, 
    but regular users only see limited fields (no ID, is_active, or is_staff).
    """

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "is_active", "is_staff"]
        extra_kwargs = {
            "is_active": {"read_only": True},
            "is_staff": {"read_only": True}, 
        }

    def to_representation(self, instance):
        """
        Remove sensitive fields if the user is not staff.
        """
        data = super().to_representation(instance)

        request = self.context.get("request")  # Ensure request exists
        if request and hasattr(request, "user") and not request.user.is_staff:
            # Remove sensitive fields for non-staff users
            data.pop("id", None)
            data.pop("is_active", None)
            data.pop("is_staff", None)

        return data



class AdminUserSerializer(serializers.ModelSerializer):
    """
    Serializer for admin users, allowing full control over users.
    """
    password = serializers.CharField(write_only=True, required=False)  # ❗ Torna a senha opcional no update

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "is_active", "is_staff", "password"]
        extra_kwargs = {
            "password": {"write_only": True, "required": False},  # ❗ Importante para tornar opcional
        }

    def create(self, validated_data):
        """
        Override create method to properly hash passwords before saving.
        """
        password = validated_data.pop("password", None)
        user = self.Meta.model(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user
    

    def update(self, instance, validated_data):
        """
        Override update method to properly hash passwords when updated.
        """
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)  # Se a senha foi enviada, hashea antes de salvar
        instance.save()
        return instance



class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for changing password.
    """
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)

    def validate_old_password(self, value):
        """
        Check if old password is correct.
        """
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

    def update(self, instance, validated_data):
        """
        Update password.
        """
        instance.set_password(validated_data["new_password"])
        instance.save()
        return instance
