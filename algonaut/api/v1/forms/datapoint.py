from algonaut.utils.forms import Form, Field
from algonaut.utils.forms.validators import Dict


class DatapointForm(Form):

    data = Field([Dict()])
