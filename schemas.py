from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date

# User Schemas
class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime

class UserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[str]

# Budget Schemas
class BudgetCreate(BaseModel):
    user_id: int
    month: str
    year: int
    target_budget: float

class BudgetUpdate(BaseModel):
    actual_spent: Optional[float]

class BudgetResponse(BaseModel):
    id: int
    user_id: int
    month: str
    year: int
    target_budget: float
    actual_spent: float
    achieved: bool
    created_at: datetime
    updated_at: datetime

# Transaction Schemas
class TransactionCreate(BaseModel):
    budget_id: int
    amount: float
    description: str
    date: date

class TransactionResponse(BaseModel):
    id: int
    budget_id: int
    amount: float
    description: str
    date: date

# Notification Schemas
class NotificationCreate(BaseModel):
    user_id: int
    month: str
    year: int
    message: str

class NotificationUpdate(BaseModel):
    message: str

class NotificationResponse(BaseModel):
    id: int
    user_id: int
    month: str
    year: int
    message: str
    created_at: datetime