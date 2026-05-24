from app.backend.db import get_connection
from pymysql.connections import Connection
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


def resource_is_active(resource_id: int) -> bool:
    sql = """
    SELECT active
    FROM resources
    WHERE id = %s
    """

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (resource_id,))
            row = cursor.fetchone()

            if row is None:
                raise RuntimeError("Expected resource row to exist")

            resource_row = cast(dict[str, Any], row)
            return bool(resource_row["active"])


def get_restaurant_tables() -> list[dict[str, Any]]:
    sql = """
    select * from resources 
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)

            return cast(list[dict[str, Any]], cursor.fetchall())


def get_available_restaurant_tables(
    start_time: str,
    end_time: str,
) -> list[dict[str, Any]]:
    sql = """
    SELECT r.*
    FROM resources r
    WHERE r.active = TRUE
      AND NOT EXISTS (
          SELECT 1
          FROM bookings b
          WHERE b.resource_id = r.id
            AND b.start_time < %s
            AND b.end_time > %s
      )
    """

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (end_time, start_time))
            return cast(list[dict[str, Any]], cursor.fetchall())


def lock_resource(resource_id: int, conn: Connection) -> None:
    sql = """
    SELECT id
    FROM resources
    WHERE id = %s
    FOR UPDATE
    """

    with conn.cursor() as cursor:
        cursor.execute(sql, (resource_id,))
        row = cursor.fetchone()

        if row is None:
            raise RuntimeError("Expected resource row to exist when locking")


def insert_booking(
    customer_id: int,
    resource_id: int,
    start_time: str,
    end_time: str,
    conn: Connection,
) -> dict:
    sql = """
        insert into bookings(customer_id, resource_id, start_time, end_time)
        values (%s, %s, %s, %s)
    """

    with conn.cursor() as cursor:
        cursor.execute(sql, (customer_id, resource_id, start_time, end_time))

        return {
            "id": cursor.lastrowid,
            "customer_id": customer_id,
            "resource_id": resource_id,
            "start_time": start_time,
            "end_time": end_time,
        }


def create_booking(
    customer_id: int, resource_id: int, start_time: str, end_time: str
) -> dict:
    with get_connection() as conn:
        booking = insert_booking(
            customer_id=customer_id,
            resource_id=resource_id,
            start_time=start_time,
            end_time=end_time,
            conn=conn,
        )
        conn.commit()
        return booking


def get_bookings() -> list[dict[str, Any]]:
    sql = """
    select * from bookings
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)

            return cast(list[dict[str, Any]], cursor.fetchall())


def get_bookings_for_resource(resource_id: int) -> list[dict[str, Any]]:
    sql = """
    SELECT *
    FROM bookings
    WHERE resource_id = %s
    ORDER BY start_time
    """

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (resource_id,))
            return cast(list[dict[str, Any]], cursor.fetchall())


def cancel_booking(booking_id: int) -> bool:
    sql = """
    DELETE FROM bookings
    WHERE id = %s
    """

    with get_connection() as conn:
        with conn.cursor() as cursor:
            deleted_rows = cursor.execute(sql, (booking_id,))
            conn.commit()
            return deleted_rows > 0


# checks if there is overlap
def has_overlapping_booking(
    resource_id: int,
    start_time: str,
    end_time: str,
    conn: Connection | None = None,
) -> bool:
    sql = """
    SELECT COUNT(*) AS count
    FROM bookings
    WHERE resource_id = %s
      AND start_time < %s
      AND end_time > %s
    """

    if conn is None:
        with get_connection() as conn:
            return has_overlapping_booking(
                resource_id=resource_id,
                start_time=start_time,
                end_time=end_time,
                conn=conn,
            )

    with conn.cursor() as cursor:
        cursor.execute(sql, (resource_id, end_time, start_time))
        row = cursor.fetchone()

        if row is None:
            raise RuntimeError("Expected overlap query to return a count row")

        count_row = cast(dict[str, Any], row)
        return count_row["count"] > 0
