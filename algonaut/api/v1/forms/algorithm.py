from algonaut.utils.forms import Form, Field
from algonaut.utils.forms.validators import Dict, String, List, Optional


class AlgorithmForm(Form):

    name = Field([String()])
    tags = Field([Optional(default=[]), List([String()])])
    data = Field([Dict()])
