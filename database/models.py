from pydantic import BaseModel
from uuid import UUID, uuid4


class Manager(BaseModel):
    id: UUID
    name: str

    def __hash__(self):
        return hash(self.id)

    class Config:
        orm_mode = True