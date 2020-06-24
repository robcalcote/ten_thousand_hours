from rest_framework import serializers
from tracker.models import *

#Goal Serializer
class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = '__all__'
        