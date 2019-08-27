from algonaut.utils.forms import Form, Field
from algonaut.utils.forms.validators import String, Dict


class ResultForm(Form):

    name = Field([String()])
    data = Field([Dict()])
