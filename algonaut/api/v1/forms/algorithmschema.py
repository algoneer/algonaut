from algonaut.utils.forms import Form, Field
from algonaut.utils.forms.validators import Dict


class AlgorithmSchemaForm(Form):

    data = Field([Dict()])
