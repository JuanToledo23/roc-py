from pydantic import BaseModel, AnyHttpUrl, Field, ConfigDict


class VeriffSession(BaseModel):
    sessionUrl: AnyHttpUrl = Field(alias='url')

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )    
