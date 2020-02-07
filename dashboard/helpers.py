def get_dashboard_task_data():
    from task.models import Task

    task_dict = dict()
    task_dict['total'] = Task.objects.count()

    return task_dict

def get_dashboard_order_data():
    from order.models import Order
    order_dict = dict()
    order_dict['total'] = Order.objects.count()

    return order_dict

def get_dashboard_customor_data():
    from user.models import User
    from user.constants import CUSTOMER

    customor_dict = dict()
    customor_dict['total'] = User.objects.filter(user_type=CUSTOMER).count()

    return customor_dict


def get_dashboard_salesman_data():
    from user.models import User
    from user.constants import SALSEMAN

    customor_dict = dict()
    customor_dict['total'] = User.objects.filter(user_type=SALSEMAN).count()

    return customor_dict

def get_dashboard_revenue_data():
    
    revenue_dict = dict()
    revenue_dict['total'] = 10

    return revenue_dict