from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr, BaseModel

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

class Cookies(BaseModel):
    session_id: str

class AdminBase(SQLModel):
    first_name: str 
    last_name: str
    email: EmailStr = Field(index=True)
    province: str
    district: str
    sector: str 
    cell: str

class AdminPublic(AdminBase):
    pass 

class AdminCreate(AdminBase):
    password_hashed: str

class Admin(AdminBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    password_hashed: str
    healthcare_advisors: list["HealthcareAdvisor"] = Relationship(back_populates="admin")

class HealthcareAdvisor(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    full_name: str 
    first_name: str
    last_name: str
    province: str 
    district: str 
    sector: str 
    cell: str
    # prediction: int
    admin_id: int | None = Field(default=None, foreign_key="admin.id")
    admin: Admin | None = Relationship(back_populates="healthcare_advisors")
    stocks: list["Stock"] = Relationship(back_populates="healthcare_advisor")

class Stock(SQLModel, table=True):
    id: int|None = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    year: int 
    month: int
    stock_item_code: str
    item_category: str
    quantity: int
    status: str
    healthcare_advisor_id: int | None = Field(default = None, foreign_key="healthcareadvisor.id")
    healthcare_advisor: HealthcareAdvisor | None = Relationship(back_populates="stocks")
