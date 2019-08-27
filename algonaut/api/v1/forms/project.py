from algonaut.utils.forms import Form, Field
from algonaut.utils.forms.validators import String, Optional, Length, Dict, List
from .validators import Path


class ProjectForm(Form):

    path = Field([String(), Path()])
    name = Field([String()])
    tags = Field([Optional(default=[]), List([String()])])
    description = Field([Optional(default=""), String(), Length(min=1, max=200)])
    data = Field([Optional(), Dict()])
