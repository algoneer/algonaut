from algonaut.utils.forms import Form, Field
from algonaut.utils.forms.validators import String, Required, Dict


class ObjectRoleForm(Form):

    object_type = Field([Required(), String()])
    object_role = Field([Required(), String()])
    organization_role = Field([Required(), String()])
