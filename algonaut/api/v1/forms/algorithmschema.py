from algonaut.utils.forms import Form, Field
from algonaut.utils.forms.validators import (
    String,
    Required,
    Optional,
    JSON,
    Binary,
    UUID,
)


class AlgorithmSchemaForm(Form):

    algorithm_id = Field([Required(), UUID()])
    hash = Field([Optional(), Binary()])
    data = Field([Optional(), JSON()])
