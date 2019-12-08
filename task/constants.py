"""
=========================================================
task status constants 
=========================================================
"""
NOT_ASSIGN = 1
PENDING = 2
STARTED = 3
COMPLETED = 4
NOT_COMPLETED = 5

TASK_STATUS_CHOICES = (
    (NOT_ASSIGN,'Not Assign'),
    (PENDING,'Pending'),
    (STARTED,'Started'),
    (COMPLETED,'Completed'),
    (NOT_COMPLETED,'Not Completed'),
)

TASK_STATUS_DICT = dict(TASK_STATUS_CHOICES)