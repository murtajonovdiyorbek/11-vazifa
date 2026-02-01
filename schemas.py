from pydantic import BaseModel
from typing import Optional

class CompanyCreate(BaseModel):
    name: str
    info: str
    address: str
    phone: str

class CompanyResponse(CompanyCreate):
    id: int

    class Config:
        from_attributes = True

class BuildingCreate(BaseModel):
    name: str
    address: str
    image: Optional[str]
    sertificate: Optional[str]
    company_id: int


class BuildingResponse(BuildingCreate):
    id: int

    class Config:
        from_attributes = True