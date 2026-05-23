from app.backend.db import get_connection
from typing import Any, cast


# customer queries
def create_customer(name: str, email: str) -> dict:
    sql = """
    INSERT INTO customers (name, email)
    VALUES (%s, %s)
    """

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (name, email))
            conn.commit()

            return {
                "id": cursor.lastrowid,
                "name": name,
                "email": email,
            }


def customer_exists(customer_id: int) -> bool:
    sql = """
    SELECT COUNT(*) AS count
    FROM customers
    WHERE id = %s
    """

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (customer_id,))
            row = cursor.fetchone()
            # implement if 0

            if row is None:
                raise RuntimeError("Expected to return a count row")

            count_row = cast(dict[str, Any], row)
            return count_row["count"] > 0


def get_customers() -> list[dict[str, Any]]:
    sql = """
    select * from customers
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)

            return cast(list[dict[str, Any]], cursor.fetchall())


# ----------------------------------------------------------------------------------------
# resource queries
def create_restaurant_table(capacity: int, tablename: str, active: bool) -> dict:
    sql = """
        insert into resources(capacity, tablename, active)
        values (%s, %s, %s)
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (capacity, tablename, active))
            conn.commit()

            return {
                "id": cursor.lastrowid,
                "capacity": capacity,
                "tablename": tablename,
                "active": active,
            }


def resource_exists(resource_id: int) -> bool:
    sql = """
    SELECT COUNT(*) AS count
    FROM resources
    WHERE id = %s
    """

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (resource_id,))
            row = cursor.fetchone()

            if row is None:
                raise RuntimeError("Expected to return a count row")

            count_row = cast(dict[str, Any], row)
            return count_row["count"] > 0


def get_restaurant_tables() -> list[dict[str, Any]]:
    sql = """
    select * from resources 
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)

            return cast(list[dict[str, Any]], cursor.fetchall())


def create_booking(
    customer_id: int, resource_id: int, start_time: str, end_time: str
) -> dict:
    sql = """
        insert into bookings(customer_id, resource_id, start_time, end_time)
        values (%s, %s, %s, %s)
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (customer_id, resource_id, start_time, end_time))
            conn.commit()

            return {
                "id": cursor.lastrowid,
                "customer_id": customer_id,
                "resource_id": resource_id,
                "start_time": start_time,
                "end_time": end_time,
            }


def get_bookings() -> list[dict[str, Any]]:
    sql = """
    select * from bookings
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)

            return cast(list[dict[str, Any]], cursor.fetchall())


# checks if there is overlap
def has_overlapping_booking(
    resource_id: int,
    start_time: str,
    end_time: str,
) -> bool:
    sql = """
    SELECT COUNT(*) AS count
    FROM bookings
    WHERE resource_id = %s
      AND start_time < %s
      AND end_time > %s
    """

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (resource_id, end_time, start_time))
            row = cursor.fetchone()

            if row is None:
                raise RuntimeError("Expected overlap query to return a count row")

            count_row = cast(dict[str, Any], row)
            return count_row["count"] > 0
