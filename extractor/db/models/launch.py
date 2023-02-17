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
    tentative_max_precision = Column(String)
    upcoming = Column(Boolean, unique=False, nullable=False)
    id_mission = Column(Integer, ForeignKey('mission.id'))
    mission = relationship('Mission', back_populates='launches')
    id_rocket = Column(Integer, ForeignKey('rocket.id'))
    rocket = relationship('Rocket', back_populates='launches')
    # id_launch_links = Column(Integer, ForeignKey('launch_links.id'))
    launch_links = relationship('LaunchLinks', uselist=False, back_populates='launch')


class LaunchLinks(Base):
    id = Column(Integer, primary_key=True, index=True)
    article_link = Column(String)
    mission_patch = Column(String)
    mission_patch_small = Column(String)
    presskit = Column(String)
    reddit_campaign = Column(String)
    reddit_launch = Column(String)
    reddit_media = Column(String)
    reddit_recovery = Column(String)
    video_link = Column(String)
    wikipedia = Column(String)
    id_launch = Column(Integer, ForeignKey('launch.id'))
    launch = relationship('Launch', back_populates='launch_links')

