from core.tool import camel_to_snake, snake_to_camel


class EntityBase:
    def get_data_and_save(self):
        raise Exception("Calling Base method")

    @staticmethod
    def db_class_name(name):
        return snake_to_camel(name)

    @staticmethod
    def db_table_name(name):
        return camel_to_snake(name)
