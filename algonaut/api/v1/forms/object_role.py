from algonaut.utils.forms import Form, Field
from algonaut.utils.forms.validators import String, Required, Dict, UUID


class ObjectRoleForm(Form):

    object_id = Field([Required(), UUID()])
    object_type = Field([Required(), String()])
    organization_id = Field([Required(), UUID()])
    object_role = Field([Required(), String()])
    organization_role = Field([Required(), String()])
