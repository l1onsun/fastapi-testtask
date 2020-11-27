from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
import sqlalchemy as sa
import sqlalchemy.orm
import enum
import uuid

Base = declarative_base()


class GlobalRoleEnum(enum.Enum):
    owner = 0
    employee = 1


class ProjectRoleEnum(enum.Enum):
    admin = 0
    manager = 1


class User(Base):
    __tablename__ = 'user'
    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = sa.Column(sa.String(length=50), nullable=False)
    role = sa.Column(sa.Enum(GlobalRoleEnum), nullable=False)
    company_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey('company.id'))
    company = sa.orm.relationship("Company")


class Company(Base):
    __tablename__ = 'company'
    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = sa.Column(sa.String(length=50), nullable=False)


class Project(Base):
    __tablename__ = 'project'
    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = sa.Column(sa.String(length=30), nullable=False)


class MemberShip(Base):
    __tablename__ = 'membership'
    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey('user.id'), nullable=False)
    project_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey('project.id'), nullable=False)
    role = sa.Column(sa.Enum(ProjectRoleEnum), nullable=False)
    user = sa.orm.relationship("User")
    project = sa.orm.relationship("Project")


sa.schema.Index('user_id_index', User.id, postgresql_using='hash')
sa.schema.Index('company_id_index', Company.id, postgresql_using='hash')
sa.schema.Index('project_id_index', Project.id, postgresql_using='hash')
sa.schema.Index('membership_id_index', MemberShip.id, postgresql_using='hash')
