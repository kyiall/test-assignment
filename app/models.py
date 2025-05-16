from geoalchemy2 import Geography
from sqlalchemy import Column, Integer, DateTime, func, String, ForeignKey
from sqlalchemy.orm import relationship, backref

from app.core.db import Base


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())


class Building(BaseModel):
    __tablename__ = "building"

    id = Column(Integer, primary_key=True)
    address = Column(String(350))
    location = Column(Geography(geometry_type='POINT', srid=4326))

    organization = relationship(
        "Organization", back_populates="building", passive_deletes=True, lazy="selectin"
    )


class Activity(BaseModel):
    __tablename__ = "activity"

    id = Column(Integer, primary_key=True)
    name = Column(String(350))
    level = Column(Integer)
    parent_id = Column(Integer, ForeignKey("activity.id", ondelete="SET NULL"), nullable=True)

    parent = relationship('Activity', remote_side=[id], backref=backref('children', lazy='selectin'))
    organization_activity = relationship(
        "OrganizationActivity", back_populates="activity", passive_deletes=True, lazy="selectin"
    )


class Organization(BaseModel):
    __tablename__ = "organization"
    name = Column(String(350))
    building_id = Column(Integer, ForeignKey("building.id", ondelete="SET NULL"), nullable=True)

    building = relationship("Building", back_populates="organization", lazy="selectin")
    phone_number = relationship(
        "PhoneNumber", back_populates="organization", passive_deletes=True, lazy="selectin"
    )
    organization_activity = relationship(
        "OrganizationActivity", back_populates="organization", passive_deletes=True, lazy="selectin"
    )


class PhoneNumber(BaseModel):
    __tablename__ = "phone_number"

    id = Column(Integer, primary_key=True)
    number = Column(String(100))
    organization_id = Column(Integer, ForeignKey("organization.id", ondelete="CASCADE"))

    organization = relationship("Organization", back_populates="phone_number", lazy="selectin")


class OrganizationActivity(BaseModel):
    __tablename__ = "organization_activity"

    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey("organization.id", ondelete="CASCADE"))
    activity_id = Column(Integer, ForeignKey("activity.id", ondelete="CASCADE"))

    organization = relationship("Organization", back_populates="organization_activity", lazy="selectin")
    activity = relationship("Activity", back_populates="organization_activity", lazy="selectin")
