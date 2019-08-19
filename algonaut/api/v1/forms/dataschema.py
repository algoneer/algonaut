from algonaut.utils.forms import Form, Field
from algonaut.utils.forms.validators import Optional, Required, Dict, Binary


class DataSchemaForm(Form):

    hash = Field([Optional(), Binary()])
    data = Field([Required(), Dict()])
