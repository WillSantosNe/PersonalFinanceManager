from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model.
    Defines how category data is serialized/deserialized in the API.
    """

    class Meta:
        model = Category
        fields = ['id', 'user', 'name', 'type']
