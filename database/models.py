from pydantic import BaseModel
import uuid
from typing import List, Optional

from .orm import GlobalRoleEnum, ProjectRoleEnum, User, Membership
import random

class Manager(BaseModel):
    id: uuid.UUID
    name: str

    def __hash__(self):
        return hash(self.id)

    class Config:
        orm_mode = True

class DetailProject(BaseModel):
    name: str
    role: ProjectRoleEnum

    @classmethod
    def from_membership(cls, membership: Membership):
        return DetailProject(
            name = membership.project.name,
            role = membership.role
        )

class DetailManager(BaseModel):
    id: uuid.UUID
    name: str

    company: Optional[str]
    role: GlobalRoleEnum

    projects: List[DetailProject]

    @classmethod
    def from_user(cls, user: User):
        return DetailManager(
            id = user.id,
            name = user.name,
            company = user.company.name,
            role = user.role,

            projects = [DetailProject.from_membership(m) for m in user.memberships]
        )