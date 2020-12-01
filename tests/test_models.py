from database import orm
from typing import Dict, List, Tuple
from dataclasses import dataclass, field
import random
import uuid

reproducible_rd = random.Random()
reproducible_rd.seed(0)


def reproducible_id():
    return uuid.UUID(int=reproducible_rd.getrandbits(128))


@dataclass
class TestManager:
    name: str
    id: uuid.UUID = field(default_factory=reproducible_id)
    projects: Dict[uuid.UUID, Tuple[orm.ProjectRoleEnum, 'TestProject']] = field(default_factory=dict)
    _role: orm.GlobalRoleEnum = None
    _company: 'TestCompany' = None
    list = []

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, v: orm.GlobalRoleEnum):
        assert self._role == None, "User has two roles!"
        self._role = v

    @property
    def company(self):
        return self._company

    @company.setter
    def company(self, v: 'TestCompany'):
        assert self._company == None, "User has two Companies!"
        self._company = v

    def add_project(self, project: 'TestProject', role: orm.ProjectRoleEnum):
        assert project.id not in self.projects, f"project '{project.name}' added twice to user '{self.name}'"
        # print(f"User {self.name} add project {project.name}")
        self.projects[project.id] = (project, role)

    def to_user_orm(self) -> orm.User:
        return orm.User(id=self.id, name=self.name, role=self.role, company_id=self.company.id)

    def to_membership_orms(self) -> List[orm.Membership]:
        return [orm.Membership(user_id=self.id, project_id=project.id, role=role)
                for project, role in self.projects.values()]

    def __post_init__(self):
        TestManager.list.append(self)


@dataclass
class TestProject:
    name: str
    id: uuid.UUID = field(default_factory=reproducible_id)
    _company: 'TestCompany' = None
    list = []

    @property
    def company(self):
        return self._company

    @company.setter
    def company(self, v: 'TestCompany'):
        assert self._company == None, "Project has two Companies!"
        self._company = v

    def to_project_orm(self) -> orm.Project:
        return orm.Project(id=self.id, name=self.name, company_id=self.company.id)

    def __post_init__(self):
        TestProject.list.append(self)



@dataclass
class TestCompany:
    name: str
    managers: List[Tuple[TestManager, orm.GlobalRoleEnum]]
    projects: List[Tuple[TestProject, List[Tuple[TestManager, orm.ProjectRoleEnum]]]]
    id: uuid.UUID = field(default_factory=reproducible_id)
    list = []

    def to_company_orm(self) -> orm.Company:
        return orm.Company(id=self.id, name=self.name)

    def __post_init__(self):
        for manager, role in self.managers:
            manager.role = role
            manager.company = self
        for project, members in self.projects:
            project.company = self
            for manager, role in members:
                manager.add_project(project, role)

        TestCompany.list.append(self)
