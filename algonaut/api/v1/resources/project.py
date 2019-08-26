from algonaut.models import Project
from ..forms import ProjectForm
from .object import Objects, ObjectDetails

joins = [[Project.organization]]

Projects = Objects(Project, ProjectForm, Joins=joins)
ProjectDetails = ObjectDetails(Project, ProjectForm, Joins=joins)
