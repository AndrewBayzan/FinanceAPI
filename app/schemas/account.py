from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class AccountCreate(BaseModel):
    name: str = Field(min_length=1, max_length=30)
    initial_balance: Decimal = Field(ge=0, max_digits=10, decimal_places=2)

class AccountResponse(BaseModel):
    id: int 
    name: str = Field(min_length=1, max_length=30)
    currency: str = Field(min_length=3, max_length=5)
    initial_balance: Decimal = Field(ge=0, max_digits=10, decimal_places=2)
    created_at: datetime 

    model_config = ConfigDict(from_attributes=True)

class AccountUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=30)
