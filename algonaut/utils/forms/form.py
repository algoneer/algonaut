import datetime

from typing import List, Callable, Any, Optional, Tuple, Dict


class Field:

    default_validators: List[
        Callable[[str, Any, "Form"], Optional[Tuple[Dict[str, Any], Any, bool]]]
    ] = []

    @property
    def validators(self):
        return self.default_validators + self._validators

    def __init__(self, validators=None):
        if validators is None:
            validators = []
        self._validators = validators

    def validate(self, name, value, form):
        for validator in self.validators:
            result = validator(name, value, form)
            if result is None:
                errors, stop = [], False
            else:
                errors, value, stop = result
            if errors:
                return errors, value
            if stop:
                return [], value
        return [], value


class FormMeta(type):
    def __init__(cls, name, bases, namespace):
        fields = {}
        for key, value in namespace.items():
            if isinstance(value, Field):
                fields[key] = value
        cls.fields = fields
        super().__init__(name, bases, namespace)


class Form(metaclass=FormMeta):
    def __init__(self, t, data, is_update=False):
        self.t = t
        self.is_update = is_update
        self.raw_data = data

    @property
    def raw_data(self):
        return self._raw_data

    @raw_data.setter
    def raw_data(self, data):
        self._raw_data = data or {}
        self.data = None
        self.errors = None

    def validate(self):
        data = {}
        errors = {}
        valid = True
        self.data = None

        for name, field in self.fields.items():
            value = self.raw_data.get(name)
            if self.is_update and value is None:
                continue
            field_errors, value = field.validate(name, value, self)
            if field_errors:
                errors[name] = field_errors
                valid = False
            else:
                data[name] = value

        self.errors = errors
        if valid:
            self.data = data
        return valid
