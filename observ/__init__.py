# flake8: noqa
from .observable import *
from .collections import *
from .descriptor import *

__version__ = '0.0.1'


def observable(value):
    if not isinstance(value, ObservableMixin):
        if isinstance(value, list):
            return ObservableList(value)
        elif isinstance(value, set):
            return ObservableSet(value)
        elif isinstance(value, dict):
            return ObservableDict(value)
        # TODO: implement observation of single values like strings, ints and floats
        # else:
        #     return Observable(value)
    return value

