from algonaut.utils.forms import Form, Field
from algonaut.utils.forms.validators import String, Dict, List, Optional


class DatasetForm(Form):

    name = Field([String()])
    tags = Field([Optional(default=[]), List([String()])])
    data = Field([Dict()])
