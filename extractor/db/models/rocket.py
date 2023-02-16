from sqlalchemy import Column, Integer, String, Boolean, Float, Date
from sqlalchemy.orm import relationship

from db.base_class import Base


class Rocket(Base):
    id = Column(Integer, primary_key=True, index=True)
    external_object_id = Column(String, unique=True, nullable=False)
    active = Column(Boolean, unique=False, nullable=False)
    boosters = Column(Integer)
    cost_per_launch = Column(Integer)
    country = Column(String)
    description = Column(String)
    diameter_meters = Column(Float)
    first_flight = Column(Date)
    height_meters = Column(Float)
    landing_legs_number = Column(Integer)
    landing_legs_material = Column(String)
    mass = Column(Float)
    name = Column(String, unique=True, nullable=False)
    success_rate_pct = Column(Float)
    wikipedia = Column(String)
    # id_rocket_type
    # id_rocket_engines
    # id_rocket_payload_weights
    # id_rocket_stages


class RocketEngines(Base):
    id = Column(Integer, primary_key=True, index=True)
    # external_object_id = Column(String, unique=True, nullable=False)
    engine_loss_max = Column(String)
    layout = Column(String)
    number = Column(Integer)
    thrust_sea_level_kn = Column(Float)
    thrust_to_weight = Column(Float)
    thrust_vacuum_kn = Column(Float)
    engines_version = Column(String)
    # id_engines_propellant_1
    # id_engines_propellant_2
    # id_rocket_engines_type


class RocketType(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)


class RocketEnginesType(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

