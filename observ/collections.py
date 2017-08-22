from .observable import ObservableMixin


__all__ = ('ObservableList', 'ObservableSet', 'ObservableDict')


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


class ObservableList(list, ObservableMixin):
    def __init__(self,  *args, **kwargs):
        ObservableMixin.__init__(self)
        list.__init__(self, *args, **kwargs)
        self.__observe_elements__()

    def changed(self, *args, **kwargs):
        self.notify(new_value=self)

    def __observe_elements__(self):
        for i in range(len(self)):
            val = list.__getitem__(self, i)
            obs_val = observable(val)
            if isinstance(obs_val, ObservableMixin) and not obs_val.is_subscribed(self.changed):
                obs_val.subscribe(self.changed)
                list.__setitem__(self, i, obs_val)


class ObservableSet(set, ObservableMixin):
    def __init__(self,  *args, **kwargs):
        ObservableMixin.__init__(self)
        set.__init__(self, *args, **kwargs)
        self.__observe_elements__()

    def changed(self, *args, **kwargs):
        self.notify(new_value=self)

    def __observe_elements__(self):
        for val in set.copy(self):
            obs_val = observable(val)
            if isinstance(obs_val, ObservableMixin) and not obs_val.is_subscribed(self.changed):
                obs_val.subscribe(self.changed)
                set.remove(self, val)
                set.add(self, obs_val)

    def __repr__(self):
        return "{" + ", ".join(map(repr, self)) + "}"


class ObservableDict(dict, ObservableMixin):
    def __init__(self, *args, **kwargs):
        ObservableMixin.__init__(self)
        dict.__init__(self, *args, **kwargs)
        self.__observe_elements__()

    def changed(self, *args, **kwargs):
        self.notify(new_value=self)

    def __observe_elements__(self):
        for key in dict.keys(self):
            val = dict.__getitem__(self, key)
            obs_val = observable(val)
            if isinstance(obs_val, ObservableMixin) and not obs_val.is_subscribed(self.changed):
                obs_val.subscribe(self.changed)
                dict.__setitem__(self, key, obs_val)


# WRAP WRITE METHODS

def wrap_method(cls, method, is_insert):
    original_method = getattr(cls, method)

    def new_method(self, *args, **kwargs):
        result = original_method(self, *args, **kwargs)
        self.notify(new_value=self)
        if is_insert:
            self.__observe_elements__()
        return result
    return new_method


for m in ['append', 'insert', 'clear', '__setitem__', '__delitem__', 'extend', 'pop', 'remove', 'sort', 'reverse']:
    is_insert = m in {'append', 'insert', '__setitem__', 'extend'}
    setattr(ObservableList, m, wrap_method(list, m, is_insert))

for m in ['add', 'remove', 'clear', 'discard', 'pop', 'symmetric_difference_update', 'difference_update',
          'intersection_update', 'update']:
    is_insert = m in {'add', 'extend', 'symmetric_difference_update', 'difference_update',
                      'intersection_update', 'update'}
    setattr(ObservableSet, m, wrap_method(set, m, is_insert))

for m in ['__setitem__', '__delitem__', 'clear', 'pop', 'popitem', 'setdefault', 'update']:
    is_insert = m in {'__setitem__', 'setdefault', 'update'}
    setattr(ObservableDict, m, wrap_method(dict, m, is_insert))
