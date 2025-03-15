# Первый способ - с помощью метаклассов
class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class FirstClass(metaclass=Singleton):
    pass


# Второй способ - с помощью метода __new__ класса
class Singleton(object):
    _instances = None

    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instances, class_):
            class_._instances = object.__new__(class_, *args, **kwargs)
        return class_._instances


class SecondClass(Singleton):
    pass


# Третий способ - через механизм импортов
class SingletonClass:
    def __init__(self):
        pass


singleton_instance = SingletonClass()

# в другом файле
# from singltone import singleton_instance
# теперь singlweton_instance - это единственный экземпляр класса SingletonClass
