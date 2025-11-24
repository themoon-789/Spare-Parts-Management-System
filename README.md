# 🔧 ระบบจัดการอะไหล่ (Spare Parts Management System)

ระบบจัดการอะไหล่แบบ Multi-Site สำหรับ Field Support Engineer ที่ต้องการติดตามสต็อกอะไหล่ข้ามหลายศูนย์บริการ พร้อมระบบอนุมัติคำขอและติดตาม Location (Rack) และ IOS Version

## ✨ Features

### 📊 Dashboard
- สรุปภาพรวมระบบ (จำนวนศูนย์, อะไหล่, สต็อกต่ำ, คำขอรออนุมัติ)
- แสดงรายการสต็อกต่ำแบบ Real-time
- รายการคำขอรออนุมัติพร้อมปุ่มอนุมัติ/ปฏิเสธ

### 📦 Inventory Management
- ติดตามสต็อกแยกตามศูนย์บริการ
- แสดง Location (Rack Number) และ IOS Version
- Highlight สต็อกต่ำด้วยสีเหลือง
- ปรับปรุงสต็อก (เพิ่ม/ลด)
- Export ข้อมูลเป็น CSV

### 🔄 Movement Tracking
- บันทึกประวัติการเคลื่อนไหวทั้งหมด
- ประเภท: ซื้อเข้า, โอนย้าย, เบิกใช้, คืนสต็อก, ปรับปรุง
- Badge สีแยกตามประเภท
- Filter ตามศูนย์และประเภท
- Export ประวัติเป็น CSV

### 📋 Request & Approval Workflow
- สร้างคำขอเบิกอะไหล่
- ระบบอนุมัติ/ปฏิเสธด้วย Custom Modal
- 6 Approvers: siraphop, Decho, Tin, Kriangkrai, Veerapot, Arom
- ติดตามสถานะ: รออนุมัติ, อนุมัติแล้ว, ปฏิเสธ
- บันทึกเหตุผลในการปฏิเสธ

### 🏢 Sites Management
- จัดการศูนย์บริการหลายแห่ง
- บันทึกข้อมูล: รหัสศูนย์, ชื่อ, จังหวัด, ที่อยู่, ผู้ติดต่อ, เบอร์โทร

### 🔧 Parts Management
- จัดการรายการอะไหล่
- บันทึก: Part Number, ชื่อ, แบรนด์, รุ่น
- **Location (Rack Number)** - ตำแหน่งจัดเก็บ
- **IOS Version** - เวอร์ชันซอฟต์แวร์/เฟิร์มแวร์
- สต็อกขั้นต่ำ (Min Stock Level)
- **ไม่มีการบันทึกราคา** - เหมาะสำหรับ Field Support

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM สำหรับจัดการฐานข้อมูล
- **SQLite** - ฐานข้อมูลแบบ Embedded
- **Pydantic** - Data validation

### Frontend
- **Vanilla JavaScript** - ไม่ใช้ Framework
- **HTML5 + CSS3** - Modern responsive design
- **Fetch API** - RESTful API calls

## 📥 Installation

### วิธีที่ 1: ติดตั้งแบบปกติ

#### 1. Clone Repository
```bash
git clone <repository-url>
cd spare-parts-system
```

#### 2. ติดตั้ง Python Dependencies
```bash
cd backend
pip install -r requirements.txt
```

#### 3. รัน Backend
```bash
uvicorn main:app --reload
```
Backend จะทำงานที่: `http://localhost:8000`

#### 4. เปิด Frontend
เปิดไฟล์ `frontend/index.html` ในเบราว์เซอร์

หรือใช้ Python HTTP Server:
```bash
cd frontend
python -m http.server 8080
```
Frontend จะทำงานที่: `http://localhost:8080`

#### 5. โหลดข้อมูลตัวอย่าง (Optional)
```bash
cd ..
pip install requests
python sample_data.py
```

### วิธีที่ 2: ใช้ Docker (Coming Soon)

```bash
docker-compose up -d
```

## 🚀 การใช้งาน

### 1. Dashboard
- เปิดระบบจะเห็นหน้า Dashboard แสดงสรุปภาพรวม
- ดูรายการสต็อกต่ำและคำขอรออนุมัติ
- คลิกปุ่ม "อนุมัติ" หรือ "ปฏิเสธ" เพื่อจัดการคำขอ

### 2. Inventory
- เลือก Tab "Inventory"
- Filter ตามศูนย์ที่ต้องการ
- คลิก "ปรับปรุงสต็อก" เพื่อเพิ่ม/ลดสต็อก
- คลิก "Export" เพื่อดาวน์โหลดข้อมูลเป็น CSV

### 3. Movements
- เลือก Tab "Movements"
- ดูประวัติการเคลื่อนไหวทั้งหมด
- Filter ตามศูนย์หรือประเภท
- Export ประวัติเป็น CSV

### 4. Requests
- เลือก Tab "Requests"
- คลิก "สร้างคำขอใหม่" เพื่อขอเบิกอะไหล่
- Filter ตามสถานะ (รออนุมัติ, อนุมัติแล้ว, ปฏิเสธ)

### 5. Sites
- เลือก Tab "Sites"
- คลิก "เพิ่มศูนย์ใหม่" เพื่อเพิ่มศูนย์บริการ
- กรอกข้อมูล: รหัสศูนย์, ชื่อ, จังหวัด, ที่อยู่, ผู้ติดต่อ, เบอร์โทร

### 6. Parts
- เลือก Tab "Parts"
- คลิก "เพิ่มอะไหล่ใหม่"
- กรอกข้อมูล: Part Number, ชื่อ, แบรนด์, รุ่น, Location (Rack), IOS Version, สต็อกขั้นต่ำ

## 📡 API Endpoints

### Sites
- `POST /sites/` - สร้างศูนย์บริการ
- `GET /sites/` - ดึงรายการศูนย์ทั้งหมด
- `GET /sites/{id}` - ดึงข้อมูลศูนย์ตาม ID

### Parts
- `POST /parts/` - สร้างอะไหล่
- `GET /parts/` - ดึงรายการอะไหล่ (มี search, filter)
- `GET /parts/{id}` - ดึงข้อมูลอะไหล่ตาม ID

### Inventory
- `GET /inventory/` - ดึงข้อมูลสต็อก (filter: site_id, low_stock)
- `POST /inventory/adjust` - ปรับปรุงสต็อก
- `POST /inventory/transfer` - โอนย้ายสต็อกระหว่างศูนย์

### Movements
- `GET /movements/` - ดึงประวัติการเคลื่อนไหว (filter: site_id, part_id, type)

### Requests
- `POST /requests/` - สร้างคำขอเบิก
- `GET /requests/` - ดึงรายการคำขอ (filter: site_id, status)
- `PUT /requests/{id}/approve` - อนุมัติคำขอ
- `PUT /requests/{id}/reject` - ปฏิเสธคำขอ

### Dashboard
- `GET /dashboard/summary` - สรุปภาพรวมระบบ

### Export
- `GET /export/inventory` - Export สต็อกเป็น CSV
- `GET /export/movements` - Export ประวัติเป็น CSV

## 🗄️ Database Schema

```
┌─────────────────┐
│     Sites       │
├─────────────────┤
│ id (PK)         │
│ site_code       │◄────┐
│ site_name       │     │
│ province        │     │
│ address         │     │
│ contact_person  │     │
│ phone           │     │
│ created_at      │     │
└─────────────────┘     │
                        │
┌─────────────────┐     │
│   SpareParts    │     │
├─────────────────┤     │
│ id (PK)         │◄──┐ │
│ part_number     │   │ │
│ part_name       │   │ │
│ category        │   │ │
│ brand           │   │ │
│ model           │   │ │
│ location        │   │ │  (Rack Number)
│ ios_version     │   │ │  (Software Version)
│ unit            │   │ │
│ min_stock_level │   │ │
│ description     │   │ │
│ created_at      │   │ │
└─────────────────┘   │ │
                      │ │
┌─────────────────┐   │ │
│   Inventory     │   │ │
├─────────────────┤   │ │
│ id (PK)         │   │ │
│ part_id (FK)    │───┘ │
│ site_id (FK)    │─────┘
│ quantity        │
│ last_updated    │
└─────────────────┘

┌─────────────────┐
│   Movements     │
├─────────────────┤
│ id (PK)         │
│ part_id (FK)    │───┐
│ from_site_id    │   │
│ to_site_id      │   │
│ quantity        │   │
│ movement_type   │   │  (purchase/transfer/issue/return/adjust)
│ reference_no    │   │
│ remark          │   │
│ created_by      │   │
│ created_at      │   │
└─────────────────┘   │
                      │
┌─────────────────┐   │
│    Requests     │   │
├─────────────────┤   │
│ id (PK)         │   │
│ site_id (FK)    │───┤
│ part_id (FK)    │───┘
│ quantity        │
│ requested_by    │
│ request_date    │
│ status          │  (pending/approved/rejected)
│ approved_by     │
│ approved_date   │
│ reject_reason   │
│ remark          │
└─────────────────┘
```

## 📸 Screenshots

### Dashboard
แสดงสรุปภาพรวม, สต็อกต่ำ, และคำขอรออนุมัติ

### Inventory
ติดตามสต็อกแยกตามศูนย์ พร้อม Location และ IOS Version

### Approval Modal
Custom modal สำหรับอนุมัติ/ปฏิเสธคำขอ พร้อม dropdown เลือก approver

## 🚢 Deploy

### Deploy บน VPS/Server

1. ติดตั้ง Python 3.8+
2. Clone repository
3. ติดตั้ง dependencies
4. ใช้ Gunicorn หรือ Uvicorn สำหรับ production:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

5. ใช้ Nginx เป็น Reverse Proxy
6. ตั้งค่า SSL Certificate (Let's Encrypt)

### Deploy Frontend

1. Upload ไฟล์ใน `frontend/` ไปยัง Web Server
2. แก้ไข `API_URL` ใน `app.js` ให้ชี้ไปยัง Backend URL
3. ใช้ Nginx หรือ Apache serve static files

## 🔧 Troubleshooting

### Backend ไม่สามารถเริ่มได้
```bash
# ตรวจสอบว่าติดตั้ง dependencies ครบ
pip install -r requirements.txt

# ตรวจสอบ port 8000 ว่าถูกใช้งานอยู่หรือไม่
lsof -i :8000

# ใช้ port อื่น
uvicorn main:app --port 8001
```

### Frontend ไม่สามารถเชื่อมต่อ Backend
- ตรวจสอบว่า Backend กำลังทำงานอยู่ที่ `http://localhost:8000`
- ตรวจสอบ CORS settings ใน `main.py`
- เปิด Browser Console (F12) เพื่อดู error messages

### ข้อมูลไม่แสดง
- ตรวจสอบว่าโหลด sample data แล้ว: `python sample_data.py`
- ตรวจสอบ Network tab ใน Browser DevTools
- ตรวจสอบ Backend logs

### Database Error
```bash
# ลบ database และสร้างใหม่
rm spare_parts.db
# รัน backend ใหม่ (จะสร้าง database อัตโนมัติ)
uvicorn main:app --reload
# โหลด sample data ใหม่
python sample_data.py
```

## 📝 Sample Data

ระบบมาพร้อมข้อมูลตัวอย่าง:

### 3 ศูนย์บริการ
- **BKK01** - ศูนย์บริการกรุงเทพ (Main warehouse - สต็อกเยอะ)
- **CNX01** - ศูนย์บริการเชียงใหม่ (สต็อกปานกลาง)
- **PKT01** - ศูนย์บริการภูเก็ต (สต็อกต่ำ)

### 8 รายการอะไหล่
- Switch 24 Port (Cisco Catalyst)
- Access Point WiFi 6
- Firewall PA-220
- Cat6 Cable
- Server Dell PowerEdge
- Power Supply (UPS)
- Hard Drive 4TB
- RAM 16GB DDR4

### 3 คำขอตัวอย่าง
- Phuket ขอ Switch 5 ตัว
- Phuket ขอ AP 10 ตัว
- Chiang Mai ขอ Server 1 ตัว

## 🎯 Use Cases

### Field Support Engineer
- ตรวจสอบสต็อกอะไหล่ก่อนไปงาน
- ขอเบิกอะไหล่จากศูนย์หลัก
- บันทึกการใช้อะไหล่ในงาน

### Warehouse Manager
- ติดตามสต็อกทุกศูนย์
- อนุมัติคำขอเบิกอะไหล่
- Export รายงานสต็อก

### IT Manager
- ดูภาพรวมสต็อกทั้งหมด
- ติดตาม IOS Version ของอุปกรณ์
- วางแผนจัดซื้ออะไหล่

## 🔐 Security Notes

- ระบบนี้เหมาะสำหรับใช้งานภายใน (Internal Network)
- ไม่มีระบบ Authentication (ควรเพิ่มก่อน Deploy สู่ Internet)
- ควรใช้ HTTPS ใน Production
- ควรตั้งค่า CORS ให้เฉพาะเจาะจงใน Production

## 🤝 Contributing

ยินดีรับ Pull Requests และ Issues!

## 📄 License

MIT License - ใช้งานได้อย่างอิสระ

## 📞 Support

หากมีปัญหาหรือข้อสงสัย:
1. เปิด Issue ใน GitHub
2. ตรวจสอบ Troubleshooting section
3. ดู API Documentation ที่ `http://localhost:8000/docs`

---

**Made with ❤️ for Field Support Engineers**

พัฒนาเพื่อให้การจัดการอะไหล่ข้ามหลายศูนย์บริการเป็นเรื่องง่าย 🚀
