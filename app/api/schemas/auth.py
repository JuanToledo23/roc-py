from pydantic import BaseModel, Field, EmailStr


class Login(BaseModel):
    phone: str = Field(pattern=r"^[+]52\d{10}$")
    channel: str = Field(default="sms")


class SignUp(BaseModel):
    phone: str = Field(pattern=r"^[+]52\d{10}$")
    email: EmailStr


class Verify(BaseModel):
    phone: str = Field(pattern=r"^[+]52\d{10}$")
    code: str = Field(min_length=6, max_length=6)
