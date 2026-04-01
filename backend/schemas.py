from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime

class CustomerBase(BaseModel):
    name: str
    email: EmailStr

class CustomerCreate(CustomerBase):
    password: str

class Customer(CustomerBase):
    id: int

    class Config:
        from_attributes = True

class AccountBase(BaseModel):
    account_type: str
    account_number: str
    balance: float

class AccountCreate(AccountBase):
    customer_id: int

class Account(AccountBase):
    id: int
    customer_id: int
    transactions: List["Transaction"] = []

    class Config:
        from_attributes = True

class TransactionBase(BaseModel):
    type: str
    amount: float
    description: str

class TransactionCreate(TransactionBase):
    account_id: int

class Transaction(TransactionBase):
    id: int
    account_id: int
    timestamp: datetime

    class Config:
        from_attributes = True

# Update forward refs for type hints
Account.model_rebuild()
