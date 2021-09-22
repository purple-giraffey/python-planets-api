from pydantic import BaseModel
from typing import Optional, List


class MoonBase(BaseModel):
    name: str
    diameter_km: int


class Moon(MoonBase):
    id: int
    planet_id: int

    class Config:
        orm_mode = True


class PlanetBase(BaseModel):
    name: str
    diameter_km: int
    distance_sun_au: float


class Planet(PlanetBase):
    id: int
    moons: List[Moon] = []

    class Config:
        orm_mode = True


class PlanetUpdate(BaseModel):
    name: Optional[str] = None
    diameter_km: Optional[int] = None
    distance_sun_au: Optional[float] = None
