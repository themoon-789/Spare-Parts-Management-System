from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from datetime import datetime
import models, schemas
from database import init_db, get_db

app = FastAPI(title="Spare Parts Management System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    init_db()

@app.get("/")
def read_root():
    return {"message": "Spare Parts Management System API"}

# ============ Sites APIs ============
@app.post("/sites/", response_model=schemas.Site)
def create_site(site: schemas.SiteCreate, db: Session = Depends(get_db)):
    db_site = db.query(models.Site).filter(models.Site.site_code == site.site_code).first()
    if db_site:
        raise HTTPException(status_code=400, detail="Site code already exists")
    db_site = models.Site(**site.dict())
    db.add(db_site)
    db.commit()
    db.refresh(db_site)
    return db_site

@app.get("/sites/", response_model=List[schemas.Site])
def read_sites(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    sites = db.query(models.Site).offset(skip).limit(limit).all()
    return sites

@app.get("/sites/{site_id}", response_model=schemas.Site)
def read_site(site_id: int, db: Session = Depends(get_db)):
    site = db.query(models.Site).filter(models.Site.id == site_id).first()
    if site is None:
        raise HTTPException(status_code=404, detail="Site not found")
    return site

# ============ Parts APIs ============
@app.post("/parts/", response_model=schemas.SparePart)
def create_part(part: schemas.SparePartCreate, db: Session = Depends(get_db)):
    db_part = db.query(models.SparePart).filter(models.SparePart.part_number == part.part_number).first()
    if db_part:
        raise HTTPException(status_code=400, detail="Part number already exists")
    db_part = models.SparePart(**part.dict())
    db.add(db_part)
    db.commit()
    db.refresh(db_part)
    return db_part

@app.get("/parts/", response_model=List[schemas.SparePart])
def read_parts(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.SparePart)
    
    if search:
        query = query.filter(
            or_(
                models.SparePart.part_number.contains(search),
                models.SparePart.part_name.contains(search)
            )
        )
    
    if category:
        query = query.filter(models.SparePart.category == category)
    
    parts = query.offset(skip).limit(limit).all()
    return parts

@app.get("/parts/{part_id}", response_model=schemas.SparePart)
def read_part(part_id: int, db: Session = Depends(get_db)):
    part = db.query(models.SparePart).filter(models.SparePart.id == part_id).first()
    if part is None:
        raise HTTPException(status_code=404, detail="Part not found")
    return part

# ============ Inventory APIs ============
@app.get("/inventory/", response_model=List[schemas.InventoryDetail])
def read_inventory(
    site_id: Optional[int] = None,
    low_stock: bool = False,
    db: Session = Depends(get_db)
):
    query = db.query(
        models.Inventory.id,
        models.Inventory.part_id,
        models.SparePart.part_number,
        models.SparePart.part_name,
        models.SparePart.category,
        models.SparePart.brand,
        models.SparePart.model,
        models.SparePart.location,
        models.SparePart.ios_version,
        models.SparePart.unit,
        models.SparePart.min_stock_level,
        models.Inventory.site_id,
        models.Site.site_code,
        models.Site.site_name,
        models.Inventory.quantity,
        models.Inventory.last_updated
    ).join(
        models.SparePart, models.Inventory.part_id == models.SparePart.id
    ).join(
        models.Site, models.Inventory.site_id == models.Site.id
    )
    
    if site_id:
        query = query.filter(models.Inventory.site_id == site_id)
    
    if low_stock:
        query = query.filter(models.Inventory.quantity < models.SparePart.min_stock_level)
    
    results = query.all()
    
    inventory_list = []
    for row in results:
        inventory_list.append(schemas.InventoryDetail(
            id=row.id,
            part_id=row.part_id,
            part_number=row.part_number,
            part_name=row.part_name,
            category=row.category,
            brand=row.brand,
            model=row.model,
            location=row.location,
            ios_version=row.ios_version,
            unit=row.unit,
            min_stock_level=row.min_stock_level,
            site_id=row.site_id,
            site_code=row.site_code,
            site_name=row.site_name,
            quantity=row.quantity,
            last_updated=row.last_updated
        ))
    
    return inventory_list

@app.post("/inventory/adjust")
def adjust_inventory(request: schemas.InventoryAdjustRequest, db: Session = Depends(get_db)):
    # ตรวจสอบว่า part และ site มีอยู่จริง
    part = db.query(models.SparePart).filter(models.SparePart.id == request.part_id).first()
    if not part:
        raise HTTPException(status_code=404, detail="Part not found")
    
    site = db.query(models.Site).filter(models.Site.id == request.site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    
    # หา inventory record
    inventory = db.query(models.Inventory).filter(
        models.Inventory.part_id == request.part_id,
        models.Inventory.site_id == request.site_id
    ).first()
    
    # ถ้าไม่มี inventory record ให้สร้างใหม่
    if not inventory:
        inventory = models.Inventory(
            part_id=request.part_id,
            site_id=request.site_id,
            quantity=0
        )
        db.add(inventory)
    
    # คำนวณ quantity ใหม่
    new_quantity = inventory.quantity + request.quantity
    
    # ตรวจสอบว่าสต็อกไม่ติดลบ
    if new_quantity < 0:
        raise HTTPException(status_code=400, detail="Insufficient stock")
    
    inventory.quantity = new_quantity
    inventory.last_updated = datetime.utcnow()
    
    # สร้าง Movement record
    movement = models.Movement(
        part_id=request.part_id,
        to_site_id=request.site_id if request.quantity > 0 else None,
        from_site_id=request.site_id if request.quantity < 0 else None,
        quantity=abs(request.quantity),
        movement_type=models.MovementType.ADJUST,
        remark=request.remark,
        created_by=request.created_by
    )
    db.add(movement)
    
    db.commit()
    db.refresh(inventory)
    
    return {
        "message": "Inventory adjusted successfully",
        "part_id": request.part_id,
        "site_id": request.site_id,
        "new_quantity": inventory.quantity
    }

@app.post("/inventory/transfer")
def transfer_inventory(request: schemas.InventoryTransferRequest, db: Session = Depends(get_db)):
    # ตรวจสอบว่า part และ sites มีอยู่จริง
    part = db.query(models.SparePart).filter(models.SparePart.id == request.part_id).first()
    if not part:
        raise HTTPException(status_code=404, detail="Part not found")
    
    from_site = db.query(models.Site).filter(models.Site.id == request.from_site_id).first()
    if not from_site:
        raise HTTPException(status_code=404, detail="From site not found")
    
    to_site = db.query(models.Site).filter(models.Site.id == request.to_site_id).first()
    if not to_site:
        raise HTTPException(status_code=404, detail="To site not found")
    
    if request.from_site_id == request.to_site_id:
        raise HTTPException(status_code=400, detail="Cannot transfer to the same site")
    
    # หา inventory ต้นทาง
    from_inventory = db.query(models.Inventory).filter(
        models.Inventory.part_id == request.part_id,
        models.Inventory.site_id == request.from_site_id
    ).first()
    
    if not from_inventory or from_inventory.quantity < request.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock at source site")
    
    # หา inventory ปลายทาง
    to_inventory = db.query(models.Inventory).filter(
        models.Inventory.part_id == request.part_id,
        models.Inventory.site_id == request.to_site_id
    ).first()
    
    # ถ้าไม่มี inventory ปลายทาง ให้สร้างใหม่
    if not to_inventory:
        to_inventory = models.Inventory(
            part_id=request.part_id,
            site_id=request.to_site_id,
            quantity=0
        )
        db.add(to_inventory)
    
    # ปรับปรุง inventory
    from_inventory.quantity -= request.quantity
    from_inventory.last_updated = datetime.utcnow()
    
    to_inventory.quantity += request.quantity
    to_inventory.last_updated = datetime.utcnow()
    
    # สร้าง Movement record
    movement = models.Movement(
        part_id=request.part_id,
        from_site_id=request.from_site_id,
        to_site_id=request.to_site_id,
        quantity=request.quantity,
        movement_type=models.MovementType.TRANSFER,
        reference_no=request.reference_no,
        remark=request.remark,
        created_by=request.created_by
    )
    db.add(movement)
    
    db.commit()
    
    return {
        "message": "Inventory transferred successfully",
        "part_id": request.part_id,
        "from_site_id": request.from_site_id,
        "to_site_id": request.to_site_id,
        "quantity": request.quantity
    }

# ============ Movements APIs ============
@app.get("/movements/", response_model=List[schemas.MovementDetail])
def read_movements(
    site_id: Optional[int] = None,
    part_id: Optional[int] = None,
    movement_type: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(
        models.Movement.id,
        models.Movement.part_id,
        models.SparePart.part_number,
        models.SparePart.part_name,
        models.Movement.from_site_id,
        models.Movement.to_site_id,
        models.Movement.quantity,
        models.Movement.movement_type,
        models.Movement.reference_no,
        models.Movement.remark,
        models.Movement.created_by,
        models.Movement.created_at
    ).join(
        models.SparePart, models.Movement.part_id == models.SparePart.id
    )
    
    if site_id:
        query = query.filter(
            or_(
                models.Movement.from_site_id == site_id,
                models.Movement.to_site_id == site_id
            )
        )
    
    if part_id:
        query = query.filter(models.Movement.part_id == part_id)
    
    if movement_type:
        query = query.filter(models.Movement.movement_type == movement_type)
    
    query = query.order_by(models.Movement.created_at.desc())
    results = query.offset(skip).limit(limit).all()
    
    movement_list = []
    for row in results:
        # Get from_site info
        from_site_code = None
        from_site_name = None
        if row.from_site_id:
            from_site = db.query(models.Site).filter(models.Site.id == row.from_site_id).first()
            if from_site:
                from_site_code = from_site.site_code
                from_site_name = from_site.site_name
        
        # Get to_site info
        to_site_code = None
        to_site_name = None
        if row.to_site_id:
            to_site = db.query(models.Site).filter(models.Site.id == row.to_site_id).first()
            if to_site:
                to_site_code = to_site.site_code
                to_site_name = to_site.site_name
        
        movement_list.append(schemas.MovementDetail(
            id=row.id,
            part_id=row.part_id,
            part_number=row.part_number,
            part_name=row.part_name,
            from_site_id=row.from_site_id,
            from_site_code=from_site_code,
            from_site_name=from_site_name,
            to_site_id=row.to_site_id,
            to_site_code=to_site_code,
            to_site_name=to_site_name,
            quantity=row.quantity,
            movement_type=row.movement_type,
            reference_no=row.reference_no,
            remark=row.remark,
            created_by=row.created_by,
            created_at=row.created_at
        ))
    
    return movement_list

# ============ Requests APIs ============
@app.post("/requests/", response_model=schemas.Request)
def create_request(request: schemas.RequestCreate, db: Session = Depends(get_db)):
    # ตรวจสอบว่า site และ part มีอยู่จริง
    site = db.query(models.Site).filter(models.Site.id == request.site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    
    part = db.query(models.SparePart).filter(models.SparePart.id == request.part_id).first()
    if not part:
        raise HTTPException(status_code=404, detail="Part not found")
    
    db_request = models.Request(**request.dict())
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request

@app.get("/requests/", response_model=List[schemas.RequestDetail])
def read_requests(
    site_id: Optional[int] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(
        models.Request.id,
        models.Request.site_id,
        models.Site.site_code,
        models.Site.site_name,
        models.Request.part_id,
        models.SparePart.part_number,
        models.SparePart.part_name,
        models.SparePart.category,
        models.Request.quantity,
        models.Request.requested_by,
        models.Request.request_date,
        models.Request.status,
        models.Request.approved_by,
        models.Request.approved_date,
        models.Request.reject_reason,
        models.Request.remark
    ).join(
        models.Site, models.Request.site_id == models.Site.id
    ).join(
        models.SparePart, models.Request.part_id == models.SparePart.id
    )
    
    if site_id:
        query = query.filter(models.Request.site_id == site_id)
    
    if status:
        query = query.filter(models.Request.status == status)
    
    results = query.offset(skip).limit(limit).all()
    
    request_list = []
    for row in results:
        request_list.append(schemas.RequestDetail(
            id=row.id,
            site_id=row.site_id,
            site_code=row.site_code,
            site_name=row.site_name,
            part_id=row.part_id,
            part_number=row.part_number,
            part_name=row.part_name,
            category=row.category,
            quantity=row.quantity,
            requested_by=row.requested_by,
            request_date=row.request_date,
            status=row.status,
            approved_by=row.approved_by,
            approved_date=row.approved_date,
            reject_reason=row.reject_reason,
            remark=row.remark
        ))
    
    return request_list

@app.put("/requests/{request_id}/approve")
def approve_request(request_id: int, update: schemas.RequestUpdate, db: Session = Depends(get_db)):
    db_request = db.query(models.Request).filter(models.Request.id == request_id).first()
    if not db_request:
        raise HTTPException(status_code=404, detail="Request not found")
    
    if db_request.status != models.RequestStatus.PENDING:
        raise HTTPException(status_code=400, detail="Request is not pending")
    
    db_request.status = models.RequestStatus.APPROVED
    db_request.approved_by = update.approved_by
    db_request.approved_date = datetime.utcnow()
    
    db.commit()
    db.refresh(db_request)
    
    return {"message": "Request approved successfully", "request_id": request_id}

@app.put("/requests/{request_id}/reject")
def reject_request(request_id: int, update: schemas.RequestUpdate, db: Session = Depends(get_db)):
    db_request = db.query(models.Request).filter(models.Request.id == request_id).first()
    if not db_request:
        raise HTTPException(status_code=404, detail="Request not found")
    
    if db_request.status != models.RequestStatus.PENDING:
        raise HTTPException(status_code=400, detail="Request is not pending")
    
    db_request.status = models.RequestStatus.REJECTED
    db_request.approved_by = update.approved_by
    db_request.approved_date = datetime.utcnow()
    db_request.reject_reason = update.reject_reason
    
    db.commit()
    db.refresh(db_request)
    
    return {"message": "Request rejected successfully", "request_id": request_id}

# ============ Dashboard API ============
@app.get("/dashboard/summary", response_model=schemas.DashboardSummary)
def get_dashboard_summary(db: Session = Depends(get_db)):
    # นับจำนวนศูนย์
    total_sites = db.query(models.Site).count()
    
    # นับจำนวนอะไหล่
    total_parts = db.query(models.SparePart).count()
    
    # นับจำนวนสต็อกต่ำ
    low_stock_items = db.query(models.Inventory).join(
        models.SparePart, models.Inventory.part_id == models.SparePart.id
    ).filter(
        models.Inventory.quantity < models.SparePart.min_stock_level
    ).count()
    
    # นับจำนวนคำขอที่รออนุมัติ
    pending_requests = db.query(models.Request).filter(
        models.Request.status == models.RequestStatus.PENDING
    ).count()
    
    return schemas.DashboardSummary(
        total_sites=total_sites,
        total_parts=total_parts,
        low_stock_items=low_stock_items,
        pending_requests=pending_requests
    )

# ============ Export APIs ============
from fastapi.responses import StreamingResponse
import io
import csv

@app.get("/export/inventory")
def export_inventory(site_id: Optional[int] = None, db: Session = Depends(get_db)):
    # Query inventory data
    query = db.query(
        models.Site.site_code,
        models.Site.site_name,
        models.SparePart.part_number,
        models.SparePart.part_name,
        models.SparePart.category,
        models.SparePart.brand,
        models.SparePart.location,
        models.SparePart.ios_version,
        models.Inventory.quantity,
        models.SparePart.unit,
        models.Inventory.last_updated
    ).join(
        models.SparePart, models.Inventory.part_id == models.SparePart.id
    ).join(
        models.Site, models.Inventory.site_id == models.Site.id
    )
    
    if site_id:
        query = query.filter(models.Inventory.site_id == site_id)
    
    results = query.all()
    
    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow([
        "Site Code",
        "Site Name",
        "Part Number",
        "Part Name",
        "Category",
        "Brand",
        "Location (Rack)",
        "IOS Version",
        "Quantity",
        "Unit",
        "Last Updated"
    ])
    
    # Write data
    for row in results:
        writer.writerow([
            row.site_code or "",
            row.site_name or "",
            row.part_number or "",
            row.part_name or "",
            row.category or "",
            row.brand or "",
            row.location or "",
            row.ios_version or "",
            row.quantity,
            row.unit or "",
            row.last_updated.strftime("%Y-%m-%d %H:%M:%S") if row.last_updated else ""
        ])
    
    # Prepare response
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename=inventory_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        }
    )

@app.get("/export/movements")
def export_movements(
    site_id: Optional[int] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    # Query movements data
    query = db.query(
        models.Movement.created_at,
        models.SparePart.part_number,
        models.SparePart.part_name,
        models.Movement.from_site_id,
        models.Movement.to_site_id,
        models.Movement.quantity,
        models.Movement.movement_type,
        models.Movement.reference_no,
        models.Movement.created_by,
        models.Movement.remark
    ).join(
        models.SparePart, models.Movement.part_id == models.SparePart.id
    )
    
    if site_id:
        query = query.filter(
            or_(
                models.Movement.from_site_id == site_id,
                models.Movement.to_site_id == site_id
            )
        )
    
    if start_date:
        try:
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
            query = query.filter(models.Movement.created_at >= start_dt)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid start_date format. Use YYYY-MM-DD")
    
    if end_date:
        try:
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")
            # Add one day to include the entire end date
            from datetime import timedelta
            end_dt = end_dt + timedelta(days=1)
            query = query.filter(models.Movement.created_at < end_dt)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid end_date format. Use YYYY-MM-DD")
    
    query = query.order_by(models.Movement.created_at.desc())
    results = query.all()
    
    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow([
        "Date",
        "Part Number",
        "Part Name",
        "From Site",
        "To Site",
        "Quantity",
        "Movement Type",
        "Reference No",
        "Created By",
        "Remark"
    ])
    
    # Write data
    for row in results:
        # Get from_site info
        from_site_name = ""
        if row.from_site_id:
            from_site = db.query(models.Site).filter(models.Site.id == row.from_site_id).first()
            if from_site:
                from_site_name = f"{from_site.site_code} - {from_site.site_name}"
        
        # Get to_site info
        to_site_name = ""
        if row.to_site_id:
            to_site = db.query(models.Site).filter(models.Site.id == row.to_site_id).first()
            if to_site:
                to_site_name = f"{to_site.site_code} - {to_site.site_name}"
        
        writer.writerow([
            row.created_at.strftime("%Y-%m-%d %H:%M:%S") if row.created_at else "",
            row.part_number or "",
            row.part_name or "",
            from_site_name,
            to_site_name,
            row.quantity,
            row.movement_type or "",
            row.reference_no or "",
            row.created_by or "",
            row.remark or ""
        ])
    
    # Prepare response
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename=movements_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        }
    )
