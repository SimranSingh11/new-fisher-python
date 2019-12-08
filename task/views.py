from rest_framework.permissions import AllowAny, IsAuthenticated

from base.models import BaseAPISet

from . import models
from . import serializers


class TaskAPISet(BaseAPISet):

    permission_classes = [IsAuthenticated]
    model = models.Task
    serializer_class = serializers.TaskSerializer
    search_fields = ['id' ,'task', 'assignee__first_name', 'assignee__last_name']
