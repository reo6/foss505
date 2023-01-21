from typing import Callable, Any


class Observable:
    """
    Certain properties of the foss505.Loop will be observable
    via this class. Designed to update UI with an Observer Pattern.
    """
    def __init__(self, initial: Any):
        self._value = initial
        self._observers = []

    def get(self):
        return self._value

    def set(self, new_value):
        self._value = new_value
        for f in self._observers: f()

    def observe(self, f):
        self._observers.append(f)

    value = property(fget=get, fset=set)
