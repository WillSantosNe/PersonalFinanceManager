from rest_framework import serializers
from .models import CustomUser

class UserSerializer():
    """
    Serializer for the User model.
    Defines how user data is serialized/deserialized in the API.
    """
    
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name']
