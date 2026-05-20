from fastapi import FastAPI, HTTPException

from app.backend.schemas import CustomerCreate
from app.backend.services import list_customers, register_customer

app = FastAPI()


@app.get("/")
def root():
    return {"status": "backend-heavy api running"}


@app.get("/customers")
def customers():
    return list_customers()


@app.post("/customers")
def add_customer(customer: CustomerCreate):
    try:
        return register_customer(
            name=customer.name,
            email=str(customer.email),
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
