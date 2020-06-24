from tracker.models import *
from rest_framework import viewsets, permissions
from tracker.serializers import *

# Goal Viewset
class GoalViewSet(viewsets.ModelViewSet):
    queryset = Goal.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = GoalSerializer