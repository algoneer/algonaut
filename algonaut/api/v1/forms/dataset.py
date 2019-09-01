from algonaut.utils.forms import Form, Field
from algonaut.utils.forms.validators import String, Dict, List, Optional, Binary


class DatasetForm(Form):

    name = Field([Optional(default=""), String()])
    hash = Field([Optional(), Binary()])
    tags = Field([Optional(default=[]), List([String()])])
    data = Field([Optional(default={}), Dict()])
