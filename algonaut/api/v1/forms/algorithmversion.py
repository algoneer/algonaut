from algonaut.utils.forms import Form, Field
from algonaut.utils.forms.validators import (
    String,
    Required,
    Optional,
    Dict,
    Binary,
    UUID,
)


class AlgorithmVersionForm(Form):

    algorithm_id = Field([Required(), UUID()])
    hash = Field([Optional(), Binary()])
    data = Field([Optional(), Dict()])
