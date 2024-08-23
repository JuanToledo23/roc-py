from pydantic import BaseModel


class StripeCard(BaseModel):
    id: str
    brand: str
    exp_month: int
    exp_year: int
    funding: str
    last4: str
    is_active: bool

    class Config:
        from_attributes = True
