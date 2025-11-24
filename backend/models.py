from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
import enum

class MovementType(str, enum.Enum):
    PURCHASE = "purchase"
    TRANSFER = "transfer"
    ISSUE = "issue"
    RETURN = "return"
    ADJUST = "adjust"

class RequestStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class Site(Base):
    __tablename__ = "sites"

    id = Column(Integer, primary_key=True, index=True)
    site_code = Column(String(50), unique=True, index=True, nullable=False)
    site_name = Column(String(200), nullable=False)
    province = Column(String(100))
    address = Column(Text)
    contact_person = Column(String(100))
    phone = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    inventories = relationship("Inventory", back_populates="site")
    movements_from = relationship("Movement", foreign_keys="Movement.from_site_id", back_populates="from_site")
    movements_to = relationship("Movement", foreign_keys="Movement.to_site_id", back_populates="to_site")
    requests = relationship("Request", back_populates="site")

class SparePart(Base):
    __tablename__ = "spare_parts"

    id = Column(Integer, primary_key=True, index=True)
    part_number = Column(String(100), unique=True, index=True, nullable=False)
    part_name = Column(String(200), nullable=False)
    category = Column(String(100))
    brand = Column(String(100))
    model = Column(String(100))
    location = Column(String(50))  # Rack number
    ios_version = Column(String(50))  # Software version
    unit = Column(String(20), default="pcs")
    min_stock_level = Column(Integer, default=5)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    inventories = relationship("Inventory", back_populates="part")
    movements = relationship("Movement", back_populates="part")
    requests = relationship("Request", back_populates="part")

class Inventory(Base):
    __tablename__ = "inventories"

    id = Column(Integer, primary_key=True, index=True)
    part_id = Column(Integer, ForeignKey("spare_parts.id"), nullable=False)
    site_id = Column(Integer, ForeignKey("sites.id"), nullable=False)
    quantity = Column(Integer, default=0, nullable=False)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    part = relationship("SparePart", back_populates="inventories")
    site = relationship("Site", back_populates="inventories")

class Movement(Base):
    __tablename__ = "movements"

    id = Column(Integer, primary_key=True, index=True)
    part_id = Column(Integer, ForeignKey("spare_parts.id"), nullable=False)
    from_site_id = Column(Integer, ForeignKey("sites.id"), nullable=True)
    to_site_id = Column(Integer, ForeignKey("sites.id"), nullable=True)
    quantity = Column(Integer, nullable=False)
    movement_type = Column(Enum(MovementType), nullable=False)
    reference_no = Column(String(100))
    remark = Column(Text)
    created_by = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    part = relationship("SparePart", back_populates="movements")
    from_site = relationship("Site", foreign_keys=[from_site_id], back_populates="movements_from")
    to_site = relationship("Site", foreign_keys=[to_site_id], back_populates="movements_to")

class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey("sites.id"), nullable=False)
    part_id = Column(Integer, ForeignKey("spare_parts.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    requested_by = Column(String(100), nullable=False)
    request_date = Column(DateTime, default=datetime.utcnow)
    status = Column(Enum(RequestStatus), default=RequestStatus.PENDING)
    approved_by = Column(String(100))
    approved_date = Column(DateTime)
    reject_reason = Column(Text)
    remark = Column(Text)

    # Relationships
    site = relationship("Site", back_populates="requests")
    part = relationship("SparePart", back_populates="requests")
