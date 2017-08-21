from .collections import ObservableDict, ObservableList, ObservableSet
from .observable import ObservableMixin


__all__ = ('ObservableProperty',)


class ObservableProperty(ObservableMixin):
    def __init__(self, initial_value_generator):
        super().__init__()
        assert callable(initial_value_generator)
        self.initial_value_generator = initial_value_generator
        self.instance_values = {}

    def make_instance_notify(self, instance):
        def instance_notify(**kwargs):
            self.notify(instance=instance, **kwargs)
        return instance_notify

    def make_observable(self, instance, value):
        if isinstance(value, list):
            value = ObservableList(value)
            value.subscribe(self.make_instance_notify(instance))
        elif isinstance(value, set):
            value = ObservableSet(value)
            value.subscribe(self.make_instance_notify(instance))
        elif isinstance(value, dict):
            value = ObservableDict(value)
            value.subscribe(self.make_instance_notify(instance))
        return value

    def __get__(self, instance, owner):
        if instance is None:
            return self
        try:
            return self.instance_values[instance]
        except KeyError:
            initial_value = self.initial_value_generator()
            initial_value = self.make_observable(instance, initial_value)
            self.instance_values[instance] = initial_value
            return initial_value

    def __set__(self, instance, value):
        old_value = self.__get__(instance, None)
        value = self.make_observable(instance, value)
        self.instance_values[instance] = value
        self.notify(instance=instance, old_value=old_value, value=value)

    def __delete__(self, obj):
        raise AttributeError("can't delete attribute")
