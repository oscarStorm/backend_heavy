from fastapi import FastAPI, HTTPException

from app.backend.schemas import CustomerCreate, RestaurantTableCreate, Booking
from app.backend.services import (
    list_customers,
    list_bookings,
    list_tables,
    register_booking,
    register_customer,
    register_restaurant_table,
)

app = FastAPI()


@app.get("/")
def root():
    return {"status": "backend-heavy api running"}


# -----------------------------------------------------------------------------------------
# customers
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


# -------------------------------------------------------------------------------------------------
# resources/tables
@app.get("/resources")
def tables():
    return list_tables()


@app.post("/resources")
def add_table(table: RestaurantTableCreate):
    try:
        return register_restaurant_table(
            capacity=table.capacity,
            tablename=str(table.tablename),
            active=bool(table.active),
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


# ------------------------------------------------------------------
# bookings


@app.get("/booking")
def bookings():
    return list_bookings()


@app.post("/booking")
def book_table(booking: Booking):
    try:
        return register_booking(
            customer_id=booking.customer_id,
            resource_id=booking.resource_id,
            start_time=booking.start_time,
            end_time=booking.end_time,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
