from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List

# ============ Site Schemas ============
class SiteBase(BaseModel):
    site_code: str = Field(..., min_length=1, max_length=50, description="Site code")
    site_name: str = Field(..., min_length=1, max_length=200, description="Site name")
    province: Optional[str] = Field(None, max_length=100)
    address: Optional[str] = None
    contact_person: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)

class SiteCreate(SiteBase):
    pass

class Site(SiteBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# ============ SparePart Schemas ============
class SparePartBase(BaseModel):
    part_number: str = Field(..., min_length=1, max_length=100, description="Part number")
    part_name: str = Field(..., min_length=1, max_length=200, description="Part name")
    category: Optional[str] = Field(None, max_length=100)
    brand: Optional[str] = Field(None, max_length=100)
    model: Optional[str] = Field(None, max_length=100)
    location: Optional[str] = Field(None, max_length=50, description="Rack number")
    ios_version: Optional[str] = Field(None, max_length=50, description="Software version")
    unit: str = Field(default="pcs", max_length=20)
    min_stock_level: int = Field(default=5, ge=0, description="Minimum stock level")
    description: Optional[str] = None

class SparePartCreate(SparePartBase):
    pass

class SparePart(SparePartBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# ============ Inventory Schemas ============
class InventoryBase(BaseModel):
    part_id: int = Field(..., gt=0)
    site_id: int = Field(..., gt=0)
    quantity: int = Field(..., ge=0)

class InventoryCreate(InventoryBase):
    pass

class Inventory(InventoryBase):
    id: int
    last_updated: datetime

    class Config:
        from_attributes = True

class InventoryDetail(BaseModel):
    id: int
    part_id: int
    part_number: str
    part_name: str
    category: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    location: Optional[str] = None  # Rack number
    ios_version: Optional[str] = None  # Software version
    unit: str
    min_stock_level: int
    site_id: int
    site_code: str
    site_name: str
    quantity: int
    last_updated: datetime

    class Config:
        from_attributes = True

class InventoryAdjustRequest(BaseModel):
    part_id: int = Field(..., gt=0)
    site_id: int = Field(..., gt=0)
    quantity: int = Field(..., description="Positive to add, negative to subtract")
    remark: Optional[str] = None
    created_by: str = Field(..., min_length=1, max_length=100)

class InventoryTransferRequest(BaseModel):
    part_id: int = Field(..., gt=0)
    from_site_id: int = Field(..., gt=0)
    to_site_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)
    reference_no: Optional[str] = Field(None, max_length=100)
    remark: Optional[str] = None
    created_by: str = Field(..., min_length=1, max_length=100)
    
    @validator('to_site_id')
    def validate_different_sites(cls, v, values):
        if 'from_site_id' in values and v == values['from_site_id']:
            raise ValueError('Cannot transfer to the same site')
        return v

# ============ Movement Schemas ============
class MovementBase(BaseModel):
    part_id: int
    from_site_id: Optional[int] = None
    to_site_id: Optional[int] = None
    quantity: int
    movement_type: str  # purchase/transfer/issue/return/adjust
    reference_no: Optional[str] = None
    remark: Optional[str] = None
    created_by: Optional[str] = None

class MovementCreate(MovementBase):
    pass

class Movement(MovementBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class MovementDetail(BaseModel):
    id: int
    part_id: int
    part_number: str
    part_name: str
    from_site_id: Optional[int] = None
    from_site_code: Optional[str] = None
    from_site_name: Optional[str] = None
    to_site_id: Optional[int] = None
    to_site_code: Optional[str] = None
    to_site_name: Optional[str] = None
    quantity: int
    movement_type: str
    reference_no: Optional[str] = None
    remark: Optional[str] = None
    created_by: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

# ============ Request Schemas ============
class RequestBase(BaseModel):
    site_id: int = Field(..., gt=0)
    part_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)
    requested_by: str = Field(..., min_length=1, max_length=100)
    remark: Optional[str] = None

class RequestCreate(RequestBase):
    pass

class RequestUpdate(BaseModel):
    approved_by: str = Field(..., min_length=1, max_length=100)
    reject_reason: Optional[str] = None

class Request(RequestBase):
    id: int
    request_date: datetime
    status: str
    approved_by: Optional[str] = None
    approved_date: Optional[datetime] = None
    reject_reason: Optional[str] = None

    class Config:
        from_attributes = True

class RequestDetail(BaseModel):
    id: int
    site_id: int
    site_code: str
    site_name: str
    part_id: int
    part_number: str
    part_name: str
    category: Optional[str] = None
    quantity: int
    requested_by: str
    request_date: datetime
    status: str
    approved_by: Optional[str] = None
    approved_date: Optional[datetime] = None
    reject_reason: Optional[str] = None
    remark: Optional[str] = None

    class Config:
        from_attributes = True

# ============ Dashboard Schemas ============
class DashboardSummary(BaseModel):
    total_sites: int
    total_parts: int
    low_stock_items: int
    pending_requests: int
