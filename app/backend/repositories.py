from app.backend.db import get_connection


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


def get_customers():
    sql = """
    select * from customers
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)

            return cursor.fetchall()
