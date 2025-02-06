from rest_framework import serializers
from .models import Goal

class GoalSerializer(serializers.ModelSerializer):
    """
    Serializer for the Goal model.
    Defines how financial goals are serialized/deserialized in the API.
    """

    class Meta:
        model = Goal
        fields = ['id', 'user', 'category', 'name', 'target_amount', 'frequency']
