from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class IncomeCreate(BaseModel):
    amount: float
    date: Optional[datetime] = None
    category: str

class IncomeResponse(IncomeCreate):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class ExpenseCreate(BaseModel):
    amount: float
    date: Optional[datetime] = None
    category: str

class ExpenseResponse(ExpenseCreate):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class BudgetCreate(BaseModel):
    amount: float
    date: Optional[datetime] = None
    category: str

class BudgetResponse(BudgetCreate):
    id: int
    user_id: int

    class Config:
        orm_mode = True