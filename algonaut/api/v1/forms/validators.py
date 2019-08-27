from algonaut.settings import settings
import datetime
import re


class Path:
    def __call__(self, name, value, form):
        if not re.match(r"^([a-z0-9\-]+/)*[a-z0-9\-]+$", value):
            return ["invalid path"], None, True
        return [], value, False
