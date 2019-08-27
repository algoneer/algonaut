from algonaut.utils.forms import Form, Field
from algonaut.utils.forms.validators import Dict


class DataSchemaForm(Form):

    data = Field([Dict()])
