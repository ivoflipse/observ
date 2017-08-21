from unittest.mock import Mock

import observ


def test_set_init():
    observable = observ.ObservableSet({1, 2, 3})

    assert observable == {1, 2, 3}


def test_set_add():
    mock = Mock()

    observable = observ.ObservableSet()
    observable.subscribe(mock)

    observable.add(1)

    mock.assert_called_with(new_value={1})


def test_set_remove():
    mock = Mock()

    observable = observ.ObservableSet()
    observable.subscribe(mock)

    observable.add(1)
    mock.assert_called_with(new_value={1})

    observable.remove(1)
    mock.assert_called_with(new_value=set())


def test_set_clear():
    mock = Mock()

    observable = observ.ObservableSet()
    observable.subscribe(mock)

    observable.add(1)
    mock.assert_called_with(new_value={1})

    observable.clear()
    mock.assert_called_with(new_value=set())


def test_set_pop():
    mock = Mock()

    observable = observ.ObservableSet()
    observable.subscribe(mock)

    observable.add(1)
    mock.assert_called_with(new_value={1})

    popped = observable.pop()
    mock.assert_called_with(new_value=set())
    assert popped == 1


def test_set_discard():
    mock = Mock()

    observable = observ.ObservableSet()
    observable.subscribe(mock)

    observable.add(1)
    mock.assert_called_with(new_value={1})

    observable.discard(1)
    mock.assert_called_with(new_value=set())


def test_set_symmetric_difference_update():
    mock = Mock()

    observable = observ.ObservableSet({1, 2})
    observable.subscribe(mock)

    observable.symmetric_difference_update({2, 3})
    mock.assert_called_with(new_value={1, 3})


def test_set_difference_update():
    mock = Mock()

    observable = observ.ObservableSet({1, 2})
    observable.subscribe(mock)

    observable.difference_update({2, 3})
    mock.assert_called_with(new_value={1})


def test_set_intersection_update():
    mock = Mock()

    observable = observ.ObservableSet({1, 2})
    observable.subscribe(mock)

    observable.intersection_update({2, 3})
    mock.assert_called_with(new_value={2})


def test_set_update():
    mock = Mock()

    observable = observ.ObservableSet({1, 2})
    observable.subscribe(mock)

    observable.update({2, 3})
    mock.assert_called_with(new_value={1, 2, 3})
