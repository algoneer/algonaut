from algonaut.utils.forms import Form, Field
from algonaut.utils.forms.validators import (
    String,
    Required,
    Optional,
    Length,
    Dict,
    List,
)
from .validators import Path


class AlgorithmForm(Form):

    path = Field([Required(), String(), Path()])
    tags = Field([Optional(), List([String()])])
    description = Field([Optional(default=""), String(), Length(min=1, max=200)])
    data = Field([Optional(), Dict()])
