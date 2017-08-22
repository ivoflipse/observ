from unittest.mock import Mock

import observ


def test_nested_list():
    mock = Mock()

    root = observ.ObservableList([1, 2, 3])
    child = [4, 5, 6]
    root.append(child)

    root.subscribe(mock)
    root[3][0] = 7
    mock.assert_called_once_with(new_value=[1, 2, 3, [7, 5, 6]])


def test_nested_observable_list():
    mock = Mock()

    root = observ.ObservableList([1, 2, 3])
    child = observ.ObservableList([4, 5, 6])
    root.append(child)
    root.append(child)

    root.subscribe(mock)
    root[3][0] = 7
    mock.assert_called_once_with(new_value=[1, 2, 3, [7, 5, 6], [7, 5, 6]])

    root[4][0] = 8
    mock.assert_called_with(new_value=[1, 2, 3, [8, 5, 6], [8, 5, 6]])


def test_list_of_dicts():
    mock = Mock()

    books = observ.ObservableList([])
    got = observ.ObservableDict(title="goat", author="martin")
    books.append(got)
    lotr = observ.ObservableDict(title="lotr", author="tolkien")
    books.append(lotr)

    books.subscribe(mock)

    books[0]['title'] = "got"
    mock.assert_called_once_with(new_value=[{"title": "got", "author": "martin"}, {"title": "lotr", "author": "tolkien"}])
