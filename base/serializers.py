from rest_framework import serializers

# common validators for serializer
def validate_5mb_size(field_name, image_data):
    print('validate_5mb_size==> image_data: ', image_data)
    max_size = 1024 * 1024 * 5  # 5MB
    if image_data.size > max_size:
        error_dict = dict()
        error_dict[field_name] = 'Image too large.'
        raise serializers.ValidationError(error_dict)


def validate_image_format(field_name, image_data):
    # print('validate_image_format==> image_data: ', image_data)
    content_types = ('image/jpeg', 'image/jpg', 'image/png')
    if image_data.content_type not in content_types:
        error_dict = dict()
        error_dict[field_name] = 'File is invalid.'
        raise serializers.ValidationError(error_dict)


def validate_file_format(field_name, file_data):
    # print('validate_image_format==> file_data: ', file_data)
    content_types = ('application/pdf', 'application/msword',
                        'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'image/jpeg',
                        'image/jpg', 'image/png')

    if file_data.content_type not in content_types:
        error_dict = dict()
        error_dict[field_name] = 'File is invalid.'
        raise serializers.ValidationError(error_dict)