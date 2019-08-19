from algonaut.utils.forms import Form, Field
from algonaut.utils.forms.validators import Required, Optional, Dict, Binary, UUID


class ModelForm(Form):

    algorithmversion_id = Field([Required(), UUID()])
    hash = Field([Optional(), Binary()])
    data = Field([Required(), Dict()])
