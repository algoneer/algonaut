from algonaut.utils.forms import Form, Field
from algonaut.utils.forms.validators import String, Required, Optional, Binary, Dict


class ResultForm(Form):

    name = Field([Required(), String()])
    data = Field([Optional(), Dict()])
