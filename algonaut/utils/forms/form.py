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
        self._raw_data = data

    @property
    def raw_data(self):
        return self._raw_data

    @property
    def valid_data(self) -> Dict[str, Any]:
        return self._valid_data

    @property
    def errors(self) -> Optional[Dict[str, List[str]]]:
        return self._errors

    @raw_data.setter  # type: ignore
    def raw_data(self, data: Optional[Dict[str, Any]]):
        self._raw_data = data or {}
        self._valid_data: Dict[str, Any] = {}
        self._errors: Optional[Dict[str, List[str]]] = None

    def validate(self):
        data: Dict[str, Any] = {}
        errors: Dict[str, List[str]] = {}
        valid = True
        self._valid_data = None

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

        self._errors = errors
        if valid:
            self._valid_data = data
        return valid
