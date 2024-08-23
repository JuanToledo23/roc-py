from typing import Any, Annotated

from pydantic import BaseModel, GetCoreSchemaHandler
from pydantic_core import core_schema
from pydantic._internal import _repr
from geoalchemy2 import WKTElement

from .location import Location


class _PointPydanticAnnotation(_repr.Representation):
    @classmethod
    def __get_pydantic_core_schema__(
            cls,
            source_type: type[Any],
            handler: GetCoreSchemaHandler,
        ) -> core_schema.CoreSchema:
        tuple_schema = core_schema.tuple_positional_schema(
            [
                core_schema.float_schema(gt=-90, lt=90),
                core_schema.float_schema(gt=-180, lt=180),
            ],
        )
        chain_schema =  core_schema.chain_schema(
            [
                tuple_schema,
                core_schema.no_info_plain_validator_function(cls._validate_coordinates),
            ],
        ) 
        return core_schema.json_schema(chain_schema)

    @classmethod
    def _validate_coordinates(cls, coordinates: tuple[float, float]) -> WKTElement:
        return WKTElement("POINT (%s %s)" % coordinates)


type Point = Annotated[WKTElement, _PointPydanticAnnotation]


class BuildingZone(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class BuildingAmenity(BaseModel):
    id: int
    url: str
    description: str

    class Config:
        from_attributes = True


class BuildingAsset(BaseModel):
    id: int
    url: str

    class Config:
        from_attributes = True


class Building(BaseModel):
    id: int
    name: str
    description: str
    zone: BuildingZone
    address: str
    position: Location
    amenities: list[BuildingAmenity]
    assets: list[BuildingAsset]
    starting_price: float

    class Config:
        from_attributes = True
