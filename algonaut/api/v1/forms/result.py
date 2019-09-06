from algonaut.utils.forms import Form, Field
from algonaut.utils.forms.validators import String, Dict, Optional


class ResultForm(Form):

    name = Field([String()])
    version = Field([Optional(default="1.0.0"), String()])
    data = Field([Dict()])
