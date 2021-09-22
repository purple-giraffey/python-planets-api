from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from database import Base


class Planet(Base):
    __tablename__ = "planet"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String, unique=True, index=True, nullable=False)
    distance_sun_au = Column(Float(precision=4), nullable=False)
    diameter_km = Column(Integer, nullable=False)

    moons = relationship("Moon", back_populates="planet")


class Moon(Base):
    __tablename__ = "moon"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String, unique=True, index=True, nullable=False)
    diameter_km = Column(Integer, nullable=False)

    planet_id = Column(Integer, ForeignKey('planet.id'), nullable=False)
    planet = relationship("Planet", back_populates="moons")
