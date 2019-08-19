from algonaut.utils.forms import Form, Field
from algonaut.utils.forms.validators import (
    String,
    Required,
    Optional,
    Dict,
    List,
    Binary,
    UUID,
)


class DatapointForm(Form):

    datasetversion_ids = Field([Required(), List([UUID()])])
    hash = Field([Optional(), Binary()])
    data = Field([Optional(), Dict()])
