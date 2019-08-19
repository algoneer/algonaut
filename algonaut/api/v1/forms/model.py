from algonaut.utils.forms import Form, Field
from algonaut.utils.forms.validators import Required, Optional, JSON, Binary, UUID


class ModelForm(Form):

    algorithmversion_id = Field([Required(), UUID()])
    hash = Field([Optional(), Binary()])
    data = Field([Required(), JSON()])
