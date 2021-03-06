class NoSuchDispatchMethodException(Exception):
    pass


class TypeDispatcher(object):
    def __init__(self):
        self.__map = dict()
        self.__default = None

    def on(self, func):
        def decorator(objself, obj):
            self.dispatch(objself, obj)

        return decorator

    def when(self, cls):
        def register(func):
            self.__map[cls] = func
            return func

        return register

    def default(self, func):
        self.__default = func
        return func

    def dispatch(self, objself, obj):
        if obj.__class__ in self.__map:
            self.__map[obj.__class__](objself, obj)
        elif self.__default is not None:
            self.__default(objself, obj)
        else:
            raise NoSuchDispatchMethodException("No specific or default method registered for {}".format(obj.__class__))
