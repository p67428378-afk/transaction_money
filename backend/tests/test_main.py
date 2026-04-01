from fastapi.testclient import TestClient
from backend.main import app

def test_read_root(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "Welcome to the Transaction API"

def test_get_customer_accounts(client: TestClient):
    response = client.get("/api/v1/customer/1/accounts")
    assert response.status_code == 200
    accounts = response.json()
    assert len(accounts) == 1
    assert accounts[0]["account_type"] == "Savings"

def test_get_customer_accounts_not_found(client: TestClient):
    response = client.get("/api/v1/customer/999/accounts")
    assert response.status_code == 404
    assert response.json() == {"detail": "Accounts not found for this customer"}

def test_get_account_transactions(client: TestClient):
    response = client.get("/api/v1/customer/1/accounts/1/transactions")
    assert response.status_code == 200
    transactions = response.json()
    assert len(transactions) == 2
    assert transactions[0]["type"] == "deposit"
    assert transactions[1]["type"] == "withdrawal"

def test_get_account_transactions_not_found(client: TestClient):
    response = client.get("/api/v1/customer/1/accounts/999/transactions")
    assert response.status_code == 404
    assert response.json() == {"detail": "No transactions found for this account"}
