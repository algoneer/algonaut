from algonaut.utils.forms import Form, Field
from algonaut.utils.forms.validators import String, Dict, UUID


class ObjectRoleForm(Form):

    object_id = Field([String(), UUID()])
    organization_id = Field([String(), UUID()])
    object_type = Field([String()])
    object_role = Field([String()])
    organization_role = Field([String()])
