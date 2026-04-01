from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas
from .database import SessionLocal, engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/", response_model=str)
def read_root():
    return "Welcome to the Transaction API"

# Placeholder for customer accounts endpoint
@app.get("/api/v1/customer/{customer_id}/accounts", response_model=List[schemas.Account])
def get_customer_accounts(customer_id: int, db: Session = Depends(get_db)):
    accounts = db.query(models.Account).filter(models.Account.customer_id == customer_id).all()
    if not accounts:
        raise HTTPException(status_code=404, detail="Accounts not found for this customer")
    return accounts

# Placeholder for transaction history endpoint
@app.get("/api/v1/customer/{customer_id}/accounts/{account_id}/transactions", response_model=List[schemas.Transaction])
def get_account_transactions(
    customer_id: int,
    account_id: int,
    start_date: str = None,
    end_date: str = None,
    db: Session = Depends(get_db)
):
    # In a real application, you would filter by customer_id and account_id
    # and apply date range filtering.
    transactions = db.query(models.Transaction).filter(models.Transaction.account_id == account_id).all()
    if not transactions:
        raise HTTPException(status_code=404, detail="No transactions found for this account")
    return transactions
