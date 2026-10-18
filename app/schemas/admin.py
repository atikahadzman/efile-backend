from pydantic import BaseModel, ConfigDict

class AdminCreate(BaseModel):
    adminName: str
    adminUsername: str
    adminContactNo: str
    adminPosition: str
    adminUnit: str
    adminPassword: str


class AdminUpdate(BaseModel):
    adminName: str | None = None
    adminUsername: str | None = None
    adminContactNo: str | None = None
    adminPosition: str | None = None
    adminUnit: str | None = None
    adminPassword: str | None = None
    

class AdminResponse(BaseModel):
    adminId: int
    adminUsername: str
    adminName: str
    adminContactNo: str
    adminPosition: str
    adminUnit: str

    model_config = ConfigDict(from_attributes=True)