from unittest.mock import Mock

import observ


def test_notify():
    mock = Mock()

    observable = observ.ObservableMixin()
    observable.subscribe(mock)
    observable.notify(val=True)

    mock.assert_called_once_with(val=True)
