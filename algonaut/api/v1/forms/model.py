from algonaut.utils.forms import Form, Field
from algonaut.utils.forms.validators import Required, Optional, Dict, Binary


class ModelForm(Form):

    hash = Field([Optional(), Binary()])
    data = Field([Required(), Dict()])
