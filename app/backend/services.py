from app.backend.db import get_connection
from app.backend.repositories import (
    cancel_booking,
    create_customer,
    create_restaurant_table,
    customer_exists,
    get_available_restaurant_tables,
    get_bookings,
    get_bookings_for_resource,
    get_customers,
    get_restaurant_tables,
    has_overlapping_booking,
    insert_booking,
    lock_resource,
    resource_is_active,
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


def list_available_tables(start_time: str, end_time: str) -> list[dict[str, Any]]:
    if start_time >= end_time:
        raise ValueError("Booking start_time must be before end_time")

    return get_available_restaurant_tables(start_time=start_time, end_time=end_time)


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

    if not resource_is_active(resource_id):
        raise ValueError("Resource is inactive")

    if start_time >= end_time:
        raise ValueError("Booking start_time must be before end_time")

    with get_connection() as conn:
        lock_resource(resource_id=resource_id, conn=conn)

        if has_overlapping_booking(
            resource_id=resource_id,
            start_time=start_time,
            end_time=end_time,
            conn=conn,
        ):
            raise ValueError("Booking overlaps an existing booking for this resource")

        booking = insert_booking(
            customer_id=customer_id,
            resource_id=resource_id,
            start_time=start_time,
            end_time=end_time,
            conn=conn,
        )
        conn.commit()
        return booking


def list_bookings() -> list[dict[str, Any]]:
    return get_bookings()


def list_bookings_for_table(resource_id: int) -> list[dict[str, Any]]:
    if not resource_exists(resource_id):
        raise ValueError("Resource does not exist")

    return get_bookings_for_resource(resource_id=resource_id)


def remove_booking(booking_id: int) -> None:
    if booking_id < 1:
        raise ValueError("Booking id must be at least 1")

    if not cancel_booking(booking_id=booking_id):
        raise ValueError("Booking does not exist")
