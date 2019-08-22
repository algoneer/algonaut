from algonaut.utils.forms import Form, Field
from algonaut.utils.forms.validators import String, Required, Dict, UUID


class ObjectRoleForm(Form):

    object_id = Field([Required(), String(), UUID()])
    #    organization_id = Field([Required(), String(), UUID()])
    object_type = Field([Required(), String()])
    object_role = Field([Required(), String()])
    organization_role = Field([Required(), String()])
