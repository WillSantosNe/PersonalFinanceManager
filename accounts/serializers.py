from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    Defines how user data is serialized/deserialized in the API.
    """
    
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name']


class AdminUserSerializer(serializers.ModelSerializer):
    """
    Serializer for admin users (shows more details).
    """
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'is_active', 'is_staff']
