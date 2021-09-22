import crud
import models
import schemas
from database import SessionLocal, engine

from sqlalchemy.orm import Session
from fastapi import FastAPI, Path, Depends, HTTPException
from typing import Optional, List

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    # generate a dependency, which will create a new SQLAlchemy SessionLocal
    # that will be used in a single request, and then close it once the request is finished
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def index():
    return "Welcome to the Solar System!"


@app.get("/planets", response_model=List[schemas.Planet])
def read_planets(db: Session = Depends(get_db), name: Optional[str] = None):
    if name:
        planet = crud.get_planet_by_name(db, name)
        if not planet:
            raise HTTPException(
                404, {"Error": "Planet %s not found!" % (name)})
        return [planet]
    planets = crud.get_planets(db)
    return planets


@app.post("/planets", response_model=schemas.Planet, status_code=201)
def create_planet(planet: schemas.PlanetBase, db: Session = Depends(get_db)):
    new_planet_info = crud.create_planet(db, planet)
    if not isinstance(new_planet_info, models.Planet):
        raise HTTPException(
            400, {"Error": "The following error occured while trying to create planet: " + str(new_planet_info)})
    return new_planet_info


@app.get("/planets/{id}")
def read_planet_by_id(id: int = Path(None, description="Planet ID"), db: Session = Depends(get_db)):
    planet = crud.get_planet(db, id)
    if not planet:
        raise HTTPException(
            404, {"Error": "Planet with id %d not found!" % (id)})
    return planet


@app.put("/planet/{id}")
def update_planet(id: int, updated_planet: schemas.PlanetUpdate, db: Session = Depends(get_db)):
    updated_planet_info = crud.update_planet(db, id, updated_planet)
    if not isinstance(updated_planet_info, int):
        raise HTTPException(400, {"Error": "The following error occured while trying to update planet with id %s: " % (
            id) + str(updated_planet_info)})
    return crud.get_planet(db, id)


@app.delete("/planet/{id}")
def delete_planet(id: int, db: Session = Depends(get_db)):
    deleted_planet_id = crud.delete_planet(db, id)
    if not deleted_planet_id:
        raise HTTPException(404, "Planet with id %d not found!" % (id))
    return deleted_planet_id
