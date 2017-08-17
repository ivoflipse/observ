from unittest.mock import Mock

import observ


def test_list_init():
    observable = observ.ObservableList([1, 2, 3])

    assert observable == [1, 2, 3]


def test_list_append():
    mock = Mock()

    observable = observ.ObservableList()
    observable.subscribe(mock)

    observable.append(1)

    mock.assert_called_with(new_value=[1])


def test_list_remove():
    mock = Mock()

    observable = observ.ObservableList()
    observable.subscribe(mock)

    observable.append(1)
    mock.assert_called_with(new_value=[1])

    observable.remove(1)
    mock.assert_called_with(new_value=[])


def test_list_indexing():
    mock = Mock()

    observable = observ.ObservableList()
    observable.subscribe(mock)

    observable.append(1)
    mock.assert_called_with(new_value=[1])

    observable[0] = 5
    mock.assert_called_with(new_value=[5])


def test_list_clear():
    mock = Mock()

    observable = observ.ObservableList()
    observable.subscribe(mock)

    observable.append(1)
    mock.assert_called_with(new_value=[1])

    observable.clear()
    mock.assert_called_with(new_value=[])


def test_list_pop():
    mock = Mock()

    observable = observ.ObservableList()
    observable.subscribe(mock)

    observable.append(1)
    mock.assert_called_with(new_value=[1])

    popped = observable.pop()
    mock.assert_called_with(new_value=[])
    assert popped == 1


def test_list_delete():
    mock = Mock()

    observable = observ.ObservableList()
    observable.subscribe(mock)

    observable.append(1)
    mock.assert_called_with(new_value=[1])

    del observable[0]
    mock.assert_called_with(new_value=[])


def test_list_insert():
    mock = Mock()

    observable = observ.ObservableList()
    observable.subscribe(mock)

    observable.append(1)
    mock.assert_called_with(new_value=[1])

    observable.insert(0, 2)
    mock.assert_called_with(new_value=[2, 1])


def test_list_extend():
    mock = Mock()

    observable = observ.ObservableList()
    observable.subscribe(mock)

    observable.append(1)
    mock.assert_called_with(new_value=[1])

    observable.extend([2, 3])
    mock.assert_called_with(new_value=[1, 2, 3])


def test_list_reverse():
    mock = Mock()

    observable = observ.ObservableList([1, 2, 3])
    observable.subscribe(mock)

    observable.reverse()
    mock.assert_called_with(new_value=[3, 2, 1])


def test_list_sort():
    mock = Mock()

    observable = observ.ObservableList([1, 3, 2])
    observable.subscribe(mock)

    observable.sort()
    mock.assert_called_with(new_value=[1, 2, 3])
