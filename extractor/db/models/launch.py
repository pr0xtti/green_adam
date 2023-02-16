from sqlalchemy import Column, Integer, String, Boolean, Float, Date, ForeignKey
from sqlalchemy.orm import relationship

from db.base_class import Base


class Launch(Base):
    id = Column(Integer, primary_key=True, index=True)
    external_object_id = Column(String, unique=True, nullable=False)
    details = Column(String)
    is_tentative = Column(Boolean)
    launch_date_utc = Column(Date)
    launch_success = Column(Boolean)
    launch_year = Column(String)
    static_fire_date_utc = Column(Date)
    telemetry_flight_club = Column(String)
    tentative_max_precesion = Column(String)
    upcoming = Column(Boolean, unique=False, nullable=False)
    id_mission = Column(Integer, ForeignKey('mission.id'))
    mission = relationship('Mission', back_populates='launches')
    id_rocket = Column(Integer, ForeignKey('rocket.id'))
    rocket = relationship('Rocket', back_populates='launches')

