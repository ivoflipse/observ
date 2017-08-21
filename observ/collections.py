from .observable import ObservableMixin


__all__ = ('ObservableList', 'ObservableSet', 'ObservableDict')


class ObservableList(list, ObservableMixin):
    def __init__(self,  *args, **kwargs):
        ObservableMixin.__init__(self)
        list.__init__(self, *args, **kwargs)


class ObservableSet(set, ObservableMixin):
    def __init__(self,  *args, **kwargs):
        ObservableMixin.__init__(self)
        set.__init__(self, *args, **kwargs)

    def __repr__(self):
        return "{" + ", ".join(map(repr, self)) + "}"


class ObservableDict(dict, ObservableMixin):
    def __init__(self, *args, **kwargs):
        ObservableMixin.__init__(self)
        dict.__init__(self, *args, **kwargs)


# WRAP WRITE METHODS

def wrap_method(cls, method, is_insert):
    original_method = getattr(cls, method)

    def new_method(self, *args, **kwargs):
        result = original_method(self, *args, **kwargs)
        self.notify(new_value=self)
        if is_insert:
            pass  # TODO: make new elements observable
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
