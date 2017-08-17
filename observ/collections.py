from .observable import Observable


__all__ = ('ObservableList', 'ObservableSet', 'ObservableDict')


def make_observable(value, root_observable):
    if not isinstance(value, Observable):
        if isinstance(value, list):
            value = ObservableList(iterable=value, root_observable=root_observable)
        elif isinstance(value, set):
            value = ObservableSet(iterable=value, root_observable=root_observable)
        elif isinstance(value, dict):
            value = ObservableDict(iterable=value, root_observable=root_observable)
    return value


class ObservableList(list, Observable):
    def __init__(self, iterable=None, root_observable=None):
        Observable.__init__(self)
        if iterable is not None:
            list.__init__(self, iterable)
        else:
            list.__init__(self)

        self.root_observable = root_observable or self
        if iterable is not None:
            self.__observe_elements__()

    def __observe_elements__(self):
        for i in range(len(self)):
            value = list.__getitem__(self, i)
            observable_value = make_observable(value, self.root_observable)
            if observable_value is not value:
                list.__setitem__(self, i, observable_value)


class ObservableSet(set, Observable):
    def __init__(self, iterable=None, root_observable=None):
        Observable.__init__(self)
        if iterable is not None:
            set.__init__(self, iterable)
        else:
            set.__init__(self)

        self.root_observable = root_observable or self
        if iterable is not None:
            self.__observe_elements__()

    def __repr__(self):
        return "{" + ", ".join(map(repr, self)) + "}"

    def __observe_elements__(self):
        for value in set.copy(self):  # TODO: can this be done without copy?
            observable_value = make_observable(value, self.root_observable)
            if observable_value is not value:
                set.remove(self, value)
                set.add(self, observable_value)


class ObservableDict(dict, Observable):
    def __init__(self, iterable=None, root_observable=None, **kwargs):
        Observable.__init__(self)
        if iterable is not None:
            dict.__init__(self, iterable, **kwargs)
        else:
            dict.__init__(self, **kwargs)

        self.root_observable = root_observable or self
        if iterable is not None:
            self.__observe_elements__()

    def __observe_elements__(self):
        for key in dict.keys(self):
            value = dict.__getitem__(self, key)
            observable_value = make_observable(value, self.root_observable)
            if observable_value is not value:
                dict.__setitem__(self, key, observable_value)


def wrap_method(cls, method, inserted):
    original_method = getattr(cls, method)

    def new_method(self, *args, **kwargs):
        result = original_method(self, *args, **kwargs)
        if inserted:
            self.__observe_elements__()
        self.root_observable.notify(new_value=self.root_observable)
        return result
    return new_method


for m in ['append', 'insert', 'clear', '__setitem__', '__delitem__', 'extend', 'pop', 'remove', 'sort', 'reverse']:
    inserted = m in {'append', 'insert', '__setitem__', 'extend'}
    setattr(ObservableList, m, wrap_method(list, m, inserted))

for m in ['add', 'remove', 'clear', 'discard', 'pop', 'symmetric_difference_update', 'difference_update',
          'intersection_update', 'update']:
    inserted = m in {'add', 'extend', 'symmetric_difference_update', 'difference_update',
                     'intersection_update', 'update'}
    setattr(ObservableSet, m, wrap_method(set, m, inserted))

for m in ['__setitem__', '__delitem__', 'clear', 'pop', 'popitem', 'setdefault', 'update']:
    inserted = m in {'__setitem__', 'setdefault', 'update'}
    setattr(ObservableDict, m, wrap_method(dict, m, inserted))
