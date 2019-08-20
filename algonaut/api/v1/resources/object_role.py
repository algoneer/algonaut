from algonaut.models import ObjectRole
from ..forms import ObjectRoleForm
from .object import Objects, ObjectDetails

ObjectRoles = Objects(ObjectRole, ObjectRoleForm)
ObjectRoleDetails = ObjectDetails(ObjectRole, ObjectRoleForm)
