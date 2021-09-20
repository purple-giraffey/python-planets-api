from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


class Planet(BaseModel):
    name: str
    diameter_km: int
    sun_distance_au: float


class UpdatePlanet(BaseModel):
    name: Optional[str]
    diameter_km: Optional[int]
    sun_distance_au: Optional[float]


planets = {
    1: Planet(name="Mercury", diameter_km=4879, sun_distance_au=0.39),
    2: Planet(name="Venus", diameter_km=12104, sun_distance_au=0.72),
    3: Planet(name="Earth", diameter_km=12756, sun_distance_au=1),
    4: Planet(name="Mars", diameter_km=6792, sun_distance_au=1.52)
}


@app.get("/")
def index():
    return "Welcome!"


@app.get("/planets")
def get_planets():
    return planets


@app.get("/planet/{id}")
def get_planet(id: int = Path(None, description="Planet ID", gt=0, lt=len(planets)+1), name: Optional[bool] = None):
    if name:
        return planets[id].name
    else:
        return planets[id]


@app.post("/planet")
def create_planet(new_planet: Planet):
    for p in planets:
        if planets[p].name == new_planet.name:
            return {"Error": "Planet %s already exists!" % (new_planet.name)}
    id = len(planets)+1
    planets[id] = new_planet
    return planets[id]


@app.put("/planet/{id}")
def update_planet(id: int, updated_planet: UpdatePlanet):
    if id not in planets:
        return {"Error": "ID not found"}
    if updated_planet.name:
        planets[id].name = updated_planet.name
    if updated_planet.diameter_km:
        planets[id].diameter_km = updated_planet.diameter_km
    if updated_planet.sun_distance_au:
        planets[id].sun_distance_au = updated_planet.sun_distance_au
    return planets[id]


@app.delete("/planet/{id}")
def delete_planet(id: int):
    if id not in planets:
        return {"Error": "ID not found"}
    return planets.pop(id)
