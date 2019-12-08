from django.db import models
from base.models import BaseModel
from . import constants
from user.models import User


class Task(BaseModel):
    task = models.CharField(max_length=255, db_column='task')
    status = models.IntegerField(default=constants.PENDING, db_column='status')
    assignee = models.ForeignKey(User, blank=True, null=True, related_name='task_assignee', on_delete=models.CASCADE, db_column='assignee_id')
    issue_date = models.DateTimeField(blank=True, null=True, db_column='issue_date')
    due_date = models.DateTimeField(blank=True, null=True, db_column='due_date')

    class Meta:
        verbose_name_plural = 'Tasks'
        verbose_name = 'Task'
        db_table = 'task_master'