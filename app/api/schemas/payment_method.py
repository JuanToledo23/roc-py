from pydantic import BaseModel


class PaymentMethodCreate(BaseModel):
    is_default: bool


class PaymentMethod(BaseModel):
    id: int
    is_default: bool

    class Config:
        from_attributes = True
