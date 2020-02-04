def get_user_obj_data(obj):
    user_data = dict()
    user_data['id'] = obj.pk
    user_data['email'] = obj.email
    user_data['first_name'] = obj.first_name
    user_data['last_name'] = obj.last_name
    user_data['dial_code'] = obj.dial_code
    user_data['phone_number'] = obj.phone_number
    user_data['full_name'] = obj.get_full_name()
    # user_data['is_superuser'] = obj.is_superuser
    user_data['contact_number'] = obj.get_contact_number()
    user_data['image'] = obj.get_image_path()

    return user_data


def generate_salesman_id():
    import uuid
    return "S{}".format(str(uuid.uuid4().fields[-1])[:5])


def generate_salesman_password():
    import uuid
    return "{}".format(str(uuid.uuid4().fields[-1])[:5])


def send_registration_mail(salesman_obj):
    from my_helpers.email_thread import email_send

    password =  generate_salesman_password()
    salesman_obj.set_password(password)

    subject = "Registarion Successfull"
    message = "Password: {}".format(password)
    to_email_list = [salesman_obj.email]
    
    email_send(subject=subject, message=message, to_email_list=to_email_list)