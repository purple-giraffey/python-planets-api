from sqlalchemy.orm import Session
from sqlalchemy import update, exc
import models
import schemas


def get_planet(db: Session, planet_id: int):
    return db.query(models.Planet).filter(models.Planet.id == planet_id).first()


def get_planets(db: Session, limit: int = 100, offset: int = 0):
    return db.query(models.Planet).limit(limit).offset(offset).all()


def get_planet_by_name(db: Session, name: str):
    return db.query(models.Planet).filter(models.Planet.name == name).first()


def create_planet(db: Session, planet: schemas.PlanetBase):
    db_planet = models.Planet(
        name=planet.name, distance_sun_au=planet.distance_sun_au, diameter_km=planet.diameter_km)
    try:
        db.add(db_planet)
        db.commit()
        db.refresh(db_planet)
    except exc.SQLAlchemyError as e:
        error = e.__dict__['orig']
        return error
    return db_planet


def update_planet(db: Session, planet_id: int, updated_planet: schemas.PlanetUpdate):
    update_values = {k: v for k, v in updated_planet.dict().items() if v}
    try:
        db.query(models.Planet).filter(
            models.Planet.id == planet_id).update(values=update_values)
        db.commit()
    except exc.SQLAlchemyError as e:
        error = e.__dict__['orig']
        return error
    return planet_id


def delete_planet(db: Session, planet_id: int):
    deleted_planet_id = db.query(models.Planet).filter(models.Planet.id ==
                                                       planet_id).delete()
    db.commit()
    return deleted_planet_id


def get_moons(db: Session, limit: int = 100, offset: int = 0):
    return db.query(models.Moon).limit(limit).offset(offset).all()


def create_moon(db: Session, moon: schemas.MoonBase, planet_id: int):
    db_moon = models.Moon(**moon.dict(), planet_id=planet_id)
    db.add(db_moon)
    db.commit()
    db.refresh(db_moon)
    return db_moon
