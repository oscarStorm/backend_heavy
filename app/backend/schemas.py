from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CustomerCreate(BaseModel):
    name: str
    email: EmailStr


class RestaurantTableCreate(BaseModel):
    capacity: int
    tablename: str
    active: bool = True


class Booking(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    customer_id: int
    resource_id: int
    start_time: str
    end_time: str = Field(alias="endtime")
