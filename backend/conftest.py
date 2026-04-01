import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database import Base, get_db
from backend.main import app
from backend import models
from fastapi.testclient import TestClient

# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="session")
def engine():
    return create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

@pytest.fixture(scope="session")
def tables(engine):
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session(engine, tables):
    connection = engine.connect()
    transaction = connection.begin()
    session = sessionmaker(autocommit=False, autoflush=False, bind=connection)()

    # Add sample data
    customer = models.Customer(name="Test Customer", email="test@example.com", password_hash="hashedpassword")
    session.add(customer)
    session.commit()
    session.refresh(customer)

    account = models.Account(customer_id=customer.id, account_type="Savings", account_number="12345", balance=1000.0)
    session.add(account)
    session.commit()
    session.refresh(account)

    transaction1 = models.Transaction(account_id=account.id, type="deposit", amount=500.0, description="Initial Deposit")
    transaction2 = models.Transaction(account_id=account.id, type="withdrawal", amount=50.0, description="Groceries")
    session.add_all([transaction1, transaction2])
    session.commit()
    session.refresh(transaction1)
    session.refresh(transaction2)

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
