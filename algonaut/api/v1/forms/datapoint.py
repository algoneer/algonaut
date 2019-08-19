from algonaut.utils.forms import Form, Field
from algonaut.utils.forms.validators import (
    String,
    Required,
    Optional,
    Dict,
    List,
    Binary,
)


class DatapointForm(Form):

    hash = Field([Optional(), Binary()])
    data = Field([Optional(), Dict()])
