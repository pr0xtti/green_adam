import re


def camel_to_snake(name):
    new_name = re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()
    return new_name


def snake_to_camel(name):
    new_name = ''.join(word.title() for word in name.split('_'))
    return new_name

