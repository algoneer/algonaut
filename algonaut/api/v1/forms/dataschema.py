from algonaut.utils.forms import Form, Field
from algonaut.utils.forms.validators import Optional, Required, JSON, Binary


class DataSchemaForm(Form):

    hash = Field([Optional(), Binary()])
    data = Field([Required(), JSON()])
