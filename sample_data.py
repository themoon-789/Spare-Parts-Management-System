import requests
import json
import sys

API_URL = "http://localhost:8000"

def print_progress(message):
    print(f"✓ {message}")

def print_error(message):
    print(f"✗ {message}", file=sys.stderr)

def create_sites():
    print("\n📍 สร้างศูนย์บริการ...")
    sites = [
        {
            "site_code": "BKK01",
            "site_name": "ศูนย์บริการกรุงเทพ",
            "province": "กรุงเทพมหานคร",
            "address": "123 ถนนสุขุมวิท แขวงคลองเตย เขตคลองเตย กรุงเทพฯ 10110",
            "contact_person": "สมชาย ใจดี",
            "phone": "02-123-4567"
        },
        {
            "site_code": "CNX01",
            "site_name": "ศูนย์บริการเชียงใหม่",
            "province": "เชียงใหม่",
            "address": "456 ถนนห้วยแก้ว ตำบลสุเทพ อำเภอเมือง เชียงใหม่ 50200",
            "contact_person": "สมหญิง รักษ์ดี",
            "phone": "053-123-456"
        },
        {
            "site_code": "PKT01",
            "site_name": "ศูนย์บริการภูเก็ต",
            "province": "ภูเก็ต",
            "address": "789 ถนนภูเก็ต ตำบลตลาดใหญ่ อำเภอเมือง ภูเก็ต 83000",
            "contact_person": "สมศรี ทะเลสวย",
            "phone": "076-123-456"
        }
    ]
    
    site_ids = {}
    for site in sites:
        try:
            response = requests.post(f"{API_URL}/sites/", json=site)
            if response.status_code == 200:
                result = response.json()
                site_ids[site['site_code']] = result['id']
                print_progress(f"สร้างศูนย์ {site['site_code']} - {site['site_name']}")
            else:
                print_error(f"ไม่สามารถสร้างศูนย์ {site['site_code']}: {response.text}")
        except Exception as e:
            print_error(f"Error creating site {site['site_code']}: {e}")
    
    return site_ids

def create_parts():
    print("\n🔧 สร้างรายการอะไหล่...")
    parts = [
        {
            "part_number": "SW-001",
            "part_name": "Switch 24 Port",
            "category": "Network Equipment",
            "brand": "Cisco",
            "model": "Catalyst 2960-24TT-L",
            "location": "A-01",
            "ios_version": "15.2(4)E",
            "unit": "pcs",
            "min_stock_level": 5,
            "description": "24-port Gigabit Ethernet Switch"
        },
        {
            "part_number": "AP-001",
            "part_name": "Access Point WiFi 6",
            "category": "Network Equipment",
            "brand": "Cisco",
            "model": "Catalyst 9120AXI",
            "location": "A-02",
            "ios_version": "6.5.55",
            "unit": "pcs",
            "min_stock_level": 10,
            "description": "WiFi 6 Access Point with internal antennas"
        },
        {
            "part_number": "FW-001",
            "part_name": "Firewall PA-220",
            "category": "Security Equipment",
            "brand": "Palo Alto",
            "model": "PA-220",
            "location": "B-01",
            "ios_version": "10.2.3",
            "unit": "pcs",
            "min_stock_level": 3,
            "description": "Next-Generation Firewall"
        },
        {
            "part_number": "CB-001",
            "part_name": "Cat6 Cable",
            "category": "Cable",
            "brand": "Panduit",
            "model": "Cat6 UTP",
            "location": "Storage Room 1",
            "ios_version": "",
            "unit": "meter",
            "min_stock_level": 500,
            "description": "Category 6 UTP Cable"
        },
        {
            "part_number": "SV-001",
            "part_name": "Server Dell",
            "category": "Server",
            "brand": "Dell",
            "model": "PowerEdge R640",
            "location": "C-01",
            "ios_version": "iDRAC 4.40.00.00",
            "unit": "pcs",
            "min_stock_level": 2,
            "description": "Rack Server 1U with dual Xeon processors"
        },
        {
            "part_number": "PS-001",
            "part_name": "Power Supply",
            "category": "Power Equipment",
            "brand": "APC",
            "model": "Smart-UPS 1500VA",
            "location": "A-03",
            "ios_version": "",
            "unit": "pcs",
            "min_stock_level": 5,
            "description": "Uninterruptible Power Supply"
        },
        {
            "part_number": "HDD-001",
            "part_name": "Hard Drive 4TB",
            "category": "Storage",
            "brand": "Seagate",
            "model": "IronWolf 4TB",
            "location": "Storage Room 2",
            "ios_version": "",
            "unit": "pcs",
            "min_stock_level": 10,
            "description": "3.5-inch SATA HDD 4TB for NAS"
        },
        {
            "part_number": "RAM-001",
            "part_name": "RAM 16GB DDR4",
            "category": "Memory",
            "brand": "Kingston",
            "model": "DDR4-2666 ECC",
            "location": "Storage Room 2",
            "ios_version": "",
            "unit": "pcs",
            "min_stock_level": 20,
            "description": "16GB DDR4 ECC Memory Module"
        }
    ]
    
    part_ids = {}
    for part in parts:
        try:
            response = requests.post(f"{API_URL}/parts/", json=part)
            if response.status_code == 200:
                result = response.json()
                part_ids[part['part_number']] = result['id']
                print_progress(f"สร้างอะไหล่ {part['part_number']} - {part['part_name']}")
            else:
                print_error(f"ไม่สามารถสร้างอะไหล่ {part['part_number']}: {response.text}")
        except Exception as e:
            print_error(f"Error creating part {part['part_number']}: {e}")
    
    return part_ids

def create_inventory(site_ids, part_ids):
    print("\n📦 สร้างสต็อกเริ่มต้น...")
    
    # Bangkok - Main warehouse (high stock)
    bkk_inventory = [
        ("SW-001", 20),
        ("AP-001", 50),
        ("FW-001", 10),
        ("CB-001", 2000),
        ("SV-001", 8),
        ("PS-001", 25),
        ("HDD-001", 40),
        ("RAM-001", 100)
    ]
    
    # Chiang Mai - Medium stock
    cnx_inventory = [
        ("SW-001", 8),
        ("AP-001", 15),
        ("FW-001", 4),
        ("CB-001", 800),
        ("SV-001", 3),
        ("PS-001", 10),
        ("HDD-001", 15),
        ("RAM-001", 30)
    ]
    
    # Phuket - Low stock (below min_stock_level)
    pkt_inventory = [
        ("SW-001", 2),   # min: 5
        ("AP-001", 5),   # min: 10
        ("FW-001", 1),   # min: 3
        ("CB-001", 300), # min: 500
        ("SV-001", 1),   # min: 2
        ("PS-001", 3),   # min: 5
        ("HDD-001", 5),  # min: 10
        ("RAM-001", 10)  # min: 20
    ]
    
    inventories = [
        ("BKK01", bkk_inventory),
        ("CNX01", cnx_inventory),
        ("PKT01", pkt_inventory)
    ]
    
    for site_code, items in inventories:
        site_id = site_ids.get(site_code)
        if not site_id:
            continue
            
        for part_number, quantity in items:
            part_id = part_ids.get(part_number)
            if not part_id:
                continue
            
            try:
                data = {
                    "part_id": part_id,
                    "site_id": site_id,
                    "quantity": quantity,
                    "created_by": "System",
                    "remark": "Initial stock"
                }
                response = requests.post(f"{API_URL}/inventory/adjust", json=data)
                if response.status_code == 200:
                    print_progress(f"เพิ่มสต็อก {part_number} ที่ {site_code}: {quantity} ชิ้น")
                else:
                    print_error(f"ไม่สามารถเพิ่มสต็อก {part_number} ที่ {site_code}: {response.text}")
            except Exception as e:
                print_error(f"Error creating inventory for {part_number} at {site_code}: {e}")

def create_requests(site_ids, part_ids):
    print("\n📋 สร้างคำขอตัวอย่าง...")
    
    requests_data = [
        {
            "site_code": "PKT01",
            "part_number": "SW-001",
            "quantity": 5,
            "requested_by": "สมศรี ทะเลสวย",
            "remark": "ขอเพิ่มสต็อกเนื่องจากสต็อกต่ำ"
        },
        {
            "site_code": "PKT01",
            "part_number": "AP-001",
            "quantity": 10,
            "requested_by": "สมศรี ทะเลสวย",
            "remark": "ขยายระบบ WiFi ในอาคารใหม่"
        },
        {
            "site_code": "CNX01",
            "part_number": "SV-001",
            "quantity": 1,
            "requested_by": "สมหญิง รักษ์ดี",
            "remark": "เพิ่ม Server สำหรับ Backup"
        }
    ]
    
    for req in requests_data:
        site_id = site_ids.get(req['site_code'])
        part_id = part_ids.get(req['part_number'])
        
        if not site_id or not part_id:
            continue
        
        try:
            data = {
                "site_id": site_id,
                "part_id": part_id,
                "quantity": req['quantity'],
                "requested_by": req['requested_by'],
                "remark": req['remark']
            }
            response = requests.post(f"{API_URL}/requests/", json=data)
            if response.status_code == 200:
                print_progress(f"สร้างคำขอ: {req['site_code']} ขอ {req['part_number']} จำนวน {req['quantity']}")
            else:
                print_error(f"ไม่สามารถสร้างคำขอได้: {response.text}")
        except Exception as e:
            print_error(f"Error creating request: {e}")

def main():
    print("=" * 60)
    print("🚀 เริ่มสร้างข้อมูลตัวอย่าง - Spare Parts Management System")
    print("=" * 60)
    
    try:
        # Check if API is running
        response = requests.get(f"{API_URL}/")
        if response.status_code != 200:
            print_error("ไม่สามารถเชื่อมต่อกับ API ได้")
            print_error("กรุณาตรวจสอบว่า Backend กำลังทำงานอยู่ที่ http://localhost:8000")
            sys.exit(1)
    except Exception as e:
        print_error(f"ไม่สามารถเชื่อมต่อกับ API: {e}")
        print_error("กรุณารัน Backend ก่อน: uvicorn main:app --reload")
        sys.exit(1)
    
    # Create data
    site_ids = create_sites()
    part_ids = create_parts()
    create_inventory(site_ids, part_ids)
    create_requests(site_ids, part_ids)
    
    print("\n" + "=" * 60)
    print("✅ สร้างข้อมูลตัวอย่างเสร็จสิ้น!")
    print("=" * 60)
    print(f"\n📊 สรุป:")
    print(f"   - ศูนย์บริการ: {len(site_ids)} แห่ง")
    print(f"   - รายการอะไหล่: {len(part_ids)} รายการ")
    print(f"   - สต็อก: {len(site_ids) * len(part_ids)} รายการ")
    print(f"   - คำขอ: 3 รายการ (รออนุมัติ)")
    print(f"\n🌐 เปิดระบบได้ที่: http://localhost:8080")
    print()

if __name__ == "__main__":
    main()
