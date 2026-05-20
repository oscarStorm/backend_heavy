from app.backend.repositories import create_customer, get_customers


def list_customers() -> list[dict]:
    return get_customers()


def register_customer(name: str, email: str) -> dict:
    if len(name.strip()) < 2:
        raise ValueError("Customer name must be at least 2 characters")

    if not email.endswith("@example.com"):
        raise ValueError("Only @example.com emails are allowed")

    return create_customer(name=name.strip(), email=email.lower())
