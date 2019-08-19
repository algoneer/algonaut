from algonaut.models import ObjectRole
from ..forms import ObjectRoleForm
from .object import Objects, ObjectDetails

args = [ObjectRole, ObjectRoleForm]

ObjectRoles = Objects(*args)
ObjectRoleDetails = ObjectDetails(*args)
