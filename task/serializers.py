from rest_framework import serializers
from . import models
from base.utils import p_print


class TaskSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    task = serializers.CharField(required=True)
    assignee_id = serializers.IntegerField(required=False, allow_null=True)
    issue_date = serializers.DateTimeField(required=False, allow_null=True)
    due_date = serializers.DateTimeField(required=False, allow_null=True)
    assignee_info = serializers.SerializerMethodField()
    is_active = serializers.BooleanField(read_only=True)

    class Meta:
        model = models.Task
        fields = ('id', 'task', 'assignee_id', 'issue_date', 'due_date', 'assignee_info', 'is_active')

    def to_internal_value(self, attr_data):

        from my_helpers.datetime_helper import timestamp_to_datetime

        # p_print("before attr_data", attr_data)
        data = attr_data
        issue_date = data.get('issue_date', None)
        due_date = data.get('due_date', None)

        if issue_date:
            data['issue_date'] = timestamp_to_datetime(issue_date)

        if due_date:
            data['due_date'] = timestamp_to_datetime(due_date) 

        # p_print("after data", data)
        return super().to_internal_value(data)


    def get_assignee_info(self, obj):
        from user.helpers import get_user_obj_data
        assignee_info = get_user_obj_data(obj.assignee) if obj.assignee else dict()
        return assignee_info