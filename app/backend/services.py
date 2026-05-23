from app.backend.repositories import (
    create_customer,
    customer_exists,
    get_customers,
    create_restaurant_table,
    get_restaurant_tables,
    create_booking,
    get_bookings,
    has_overlapping_booking,
    resource_exists,
)
from typing import Any


# ---------------------------------------------------------------------------------------------------------
# customers
def list_customers() -> list[dict[str, Any]]:
    return get_customers()


def register_customer(name: str, email: str) -> dict:
    if len(name.strip()) < 2:
        raise ValueError("Customer name must be at least 2 characters")

    if not email.endswith("@example.com"):
        raise ValueError("Only @example.com emails are allowed")

    return create_customer(name=name.strip(), email=email.lower())


# -----------------------------------------------------------------------------------------------------------------
# resources/tables


def list_tables() -> list[dict[str, Any]]:
    return get_restaurant_tables()


def register_restaurant_table(capacity: int, tablename: str, active: bool) -> dict:
    if len(tablename.strip()) < 1:
        raise ValueError("Table name is required")

    if capacity < 1:
        raise ValueError("Capacity must be at least 1")

    return create_restaurant_table(
        tablename=tablename.strip(),
        capacity=capacity,
        active=active,
    )


def register_booking(
    customer_id: int, resource_id: int, start_time: str, end_time: str
) -> dict:
    if not customer_exists(customer_id):
        raise ValueError("Customer does not exist")

    if not resource_exists(resource_id):
        raise ValueError("Resource does not exist")

    if start_time >= end_time:
        raise ValueError("Booking start_time must be before end_time")

    if has_overlapping_booking(
        resource_id=resource_id,
        start_time=start_time,
        end_time=end_time,
    ):
        raise ValueError("Booking overlaps an existing booking for this resource")

    return create_booking(
        customer_id=customer_id,
        resource_id=resource_id,
        start_time=start_time,
        end_time=end_time,
    )


def list_bookings() -> list[dict[str, Any]]:
    return get_bookings()
