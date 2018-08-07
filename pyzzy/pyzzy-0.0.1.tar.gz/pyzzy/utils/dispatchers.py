from functools import singledispatch, update_wrapper


__all__ = ["predicate_dispatch", "singledispatch"]


class predicate_dispatch:

    def __init__(self, default_callback):
        self.default_callback = default_callback
        self.registry = {}
        self._instance = None
        update_wrapper(self, default_callback)

    def __get__(self, instance, cls):
        self._instance = instance
        return self

    def __call__(self, *args, **kwargs):
        callback = self.dispatch(*args, **kwargs)
        if self._instance:
            return callback(self._instance, *args, **kwargs)
        else:
            return callback(*args, **kwargs)

    def register(self, predicate, func=None):
        # If called with dispatcher.register(predicate, callback)
        if func is None:
            return lambda f: self.register(predicate, f)

        # else called with @dispatcher.register
        self.registry[predicate] = func
        return func

    def dispatch(self, *args, **kwargs):
        for predicate, callback in self.registry.items():
            if self.match(predicate, *args, **kwargs):
                return callback
        else:
            return self.default_callback

    def match(self, predicate, var, *args, **kwargs):
        try:
            return predicate(var, *args, **kwargs)
        except (AttributeError, KeyError, IndexError, TypeError, ValueError):
            return False
