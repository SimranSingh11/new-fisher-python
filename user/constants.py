"""
=========================================================
user type constants
=========================================================
"""
ADMIN = 1
SALSEMAN = 2
CUSTOMER = 3

USER_TYPE_CHOICES = (
    (ADMIN,'Admin'),
    (SALSEMAN,'Salesman'),
    (CUSTOMER,'Customer'),
)

USER_TYPE_DICT = dict(USER_TYPE_CHOICES)