from pydantic import BaseModel


class ZoneAsset(BaseModel):
    id: int
    url: str

    class Config:
        from_attributes = True


class ZonePlace(BaseModel):
    id: int
    name: str
    description: str
    # location: str

    class Config:
        from_attributes = True


class Zone(BaseModel):
    id: int
    name: str
    description: str
    assets: list[ZoneAsset]

    class Config:
        from_attributes = True
