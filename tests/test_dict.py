from unittest.mock import Mock

import observ


def test_dict_init():
    observable = observ.ObservableDict({'a': 1, 'b': 2})

    assert observable == {'a': 1, 'b': 2}


def test_dict_init_kwargs():
    observable = observ.ObservableDict(a=1, b=2)

    assert observable == {'a': 1, 'b': 2}


def test_dict_setitem():
    mock = Mock()

    observable = observ.ObservableDict()
    observable.subscribe(mock)

    observable['a'] = 1

    mock.assert_called_with(new_value={'a': 1})


def test_dict_delitem():
    mock = Mock()

    observable = observ.ObservableDict({'a': 1, 'b': 2})
    observable.subscribe(mock)

    del observable['a']
    mock.assert_called_with(new_value={'b': 2})


def test_dict_clear():
    mock = Mock()

    observable = observ.ObservableDict({'a': 1, 'b': 2})
    observable.subscribe(mock)

    observable.clear()
    mock.assert_called_with(new_value={})


def test_dict_pop():
    mock = Mock()

    observable = observ.ObservableDict({'a': 1, 'b': 2})
    observable.subscribe(mock)

    popped = observable.pop('a')
    mock.assert_called_with(new_value={'b': 2})
    assert popped == 1


def test_dict_popitem():
    mock = Mock()

    data = {'a': 1, 'b': 2}
    ref = data.copy()
    observable = observ.ObservableDict(data)
    observable.subscribe(mock)

    popped = observable.popitem()
    ref.pop(popped[0])
    mock.assert_called_with(new_value=ref)


def test_dict_setdefault():
    mock = Mock()

    observable = observ.ObservableDict({'a': 1, 'b': 2})
    observable.subscribe(mock)

    observable.setdefault('a', None)
    mock.assert_called_with(new_value={'a': 1, 'b': 2})

    observable.setdefault('c', None)
    mock.assert_called_with(new_value={'a': 1, 'b': 2, 'c': None})


def test_dict_update():
    mock = Mock()

    observable = observ.ObservableDict({'a': 1, 'b': 2})
    observable.subscribe(mock)

    observable.update({'a': 3, 'c': 4})
    mock.assert_called_with(new_value={'a': 3, 'b': 2, 'c': 4})
