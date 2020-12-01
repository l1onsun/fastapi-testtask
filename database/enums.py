import enum

class GlobalRoleEnum(enum.Enum):
    owner = "owner"
    employee = "employee"


class ProjectRoleEnum(enum.Enum):
    admin = "admin"
    manager = "manager"