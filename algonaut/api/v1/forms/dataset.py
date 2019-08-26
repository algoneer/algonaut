from algonaut.utils.forms import Form, Field
from algonaut.utils.forms.validators import (
    String,
    Required,
    Optional,
    Length,
    Dict,
    List,
    Binary,
)
from .validators import Path


class DatasetForm(Form):

    hash = Field([Optional(), Binary()])
    name = Field([Required(), String()])
    tags = Field([Optional(), List([String()])])
    data = Field([Optional(), Dict()])
