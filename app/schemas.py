from pydantic import BaseModel


class PhoneTIResponse(BaseModel):
    id: int
    phone_number: str
    ti_number: int
    email: str | None = None

    model_config = {"from_attributes": True}
