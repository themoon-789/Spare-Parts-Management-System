"""
API Testing Script for Spare Parts Management System
Run this after starting the backend server
"""
import requests
import json

API_URL = "http://localhost:8000"

def print_test(name, passed):
    status = "✓ PASS" if passed else "✗ FAIL"
    print(f"{status}: {name}")

def test_root():
    """Test root endpoint"""
    try:
        response = requests.get(f"{API_URL}/")
        print_test("GET / - Root endpoint", response.status_code == 200)
        return response.status_code == 200
    except Exception as e:
        print_test("GET / - Root endpoint", False)
        print(f"  Error: {e}")
        return False

def test_create_site():
    """Test creating a site"""
    data = {
        "site_code": "TEST01",
        "site_name": "Test Site",
        "province": "Bangkok",
        "address": "123 Test St",
        "contact_person": "Test Person",
        "phone": "02-123-4567"
    }
    try:
        response = requests.post(f"{API_URL}/sites/", json=data)
        passed = response.status_code == 200
        print_test("POST /sites/ - Create site", passed)
        if passed:
            return response.json()['id']
        return None
    except Exception as e:
        print_test("POST /sites/ - Create site", False)
        print(f"  Error: {e}")
        return None

def test_get_sites():
    """Test getting all sites"""
    try:
        response = requests.get(f"{API_URL}/sites/")
        passed = response.status_code == 200 and isinstance(response.json(), list)
        print_test("GET /sites/ - Get all sites", passed)
        return passed
    except Exception as e:
        print_test("GET /sites/ - Get all sites", False)
        print(f"  Error: {e}")
        return False

def test_create_part():
    """Test creating a part"""
    data = {
        "part_number": "TEST-001",
        "part_name": "Test Part",
        "category": "Test Category",
        "brand": "Test Brand",
        "model": "Test Model",
        "location": "A-99",
        "ios_version": "1.0.0",
        "unit": "pcs",
        "min_stock_level": 5,
        "description": "Test part for testing"
    }
    try:
        response = requests.post(f"{API_URL}/parts/", json=data)
        passed = response.status_code == 200
        print_test("POST /parts/ - Create part", passed)
        if passed:
            return response.json()['id']
        return None
    except Exception as e:
        print_test("POST /parts/ - Create part", False)
        print(f"  Error: {e}")
        return None

def test_get_parts():
    """Test getting all parts"""
    try:
        response = requests.get(f"{API_URL}/parts/")
        passed = response.status_code == 200 and isinstance(response.json(), list)
        print_test("GET /parts/ - Get all parts", passed)
        return passed
    except Exception as e:
        print_test("GET /parts/ - Get all parts", False)
        print(f"  Error: {e}")
        return False

def test_search_parts():
    """Test searching parts"""
    try:
        response = requests.get(f"{API_URL}/parts/?search=TEST")
        passed = response.status_code == 200
        print_test("GET /parts/?search=TEST - Search parts", passed)
        return passed
    except Exception as e:
        print_test("GET /parts/?search=TEST - Search parts", False)
        print(f"  Error: {e}")
        return False

def test_adjust_inventory(site_id, part_id):
    """Test adjusting inventory"""
    if not site_id or not part_id:
        print_test("POST /inventory/adjust - Adjust inventory", False)
        print("  Error: Missing site_id or part_id")
        return False
    
    data = {
        "part_id": part_id,
        "site_id": site_id,
        "quantity": 10,
        "created_by": "Test User",
        "remark": "Test adjustment"
    }
    try:
        response = requests.post(f"{API_URL}/inventory/adjust", json=data)
        passed = response.status_code == 200
        print_test("POST /inventory/adjust - Adjust inventory", passed)
        return passed
    except Exception as e:
        print_test("POST /inventory/adjust - Adjust inventory", False)
        print(f"  Error: {e}")
        return False

def test_get_inventory():
    """Test getting inventory"""
    try:
        response = requests.get(f"{API_URL}/inventory/")
        passed = response.status_code == 200 and isinstance(response.json(), list)
        print_test("GET /inventory/ - Get inventory", passed)
        return passed
    except Exception as e:
        print_test("GET /inventory/ - Get inventory", False)
        print(f"  Error: {e}")
        return False

def test_get_movements():
    """Test getting movements"""
    try:
        response = requests.get(f"{API_URL}/movements/")
        passed = response.status_code == 200 and isinstance(response.json(), list)
        print_test("GET /movements/ - Get movements", passed)
        return passed
    except Exception as e:
        print_test("GET /movements/ - Get movements", False)
        print(f"  Error: {e}")
        return False

def test_create_request(site_id, part_id):
    """Test creating a request"""
    if not site_id or not part_id:
        print_test("POST /requests/ - Create request", False)
        print("  Error: Missing site_id or part_id")
        return None
    
    data = {
        "site_id": site_id,
        "part_id": part_id,
        "quantity": 5,
        "requested_by": "Test User",
        "remark": "Test request"
    }
    try:
        response = requests.post(f"{API_URL}/requests/", json=data)
        passed = response.status_code == 200
        print_test("POST /requests/ - Create request", passed)
        if passed:
            return response.json()['id']
        return None
    except Exception as e:
        print_test("POST /requests/ - Create request", False)
        print(f"  Error: {e}")
        return None

def test_get_requests():
    """Test getting requests"""
    try:
        response = requests.get(f"{API_URL}/requests/")
        passed = response.status_code == 200 and isinstance(response.json(), list)
        print_test("GET /requests/ - Get requests", passed)
        return passed
    except Exception as e:
        print_test("GET /requests/ - Get requests", False)
        print(f"  Error: {e}")
        return False

def test_approve_request(request_id):
    """Test approving a request"""
    if not request_id:
        print_test("PUT /requests/{id}/approve - Approve request", False)
        print("  Error: Missing request_id")
        return False
    
    data = {
        "approved_by": "Test Approver"
    }
    try:
        response = requests.put(f"{API_URL}/requests/{request_id}/approve", json=data)
        passed = response.status_code == 200
        print_test("PUT /requests/{id}/approve - Approve request", passed)
        return passed
    except Exception as e:
        print_test("PUT /requests/{id}/approve - Approve request", False)
        print(f"  Error: {e}")
        return False

def test_dashboard_summary():
    """Test dashboard summary"""
    try:
        response = requests.get(f"{API_URL}/dashboard/summary")
        passed = response.status_code == 200
        if passed:
            data = response.json()
            passed = all(key in data for key in ['total_sites', 'total_parts', 'low_stock_items', 'pending_requests'])
        print_test("GET /dashboard/summary - Dashboard summary", passed)
        return passed
    except Exception as e:
        print_test("GET /dashboard/summary - Dashboard summary", False)
        print(f"  Error: {e}")
        return False

def test_export_inventory():
    """Test exporting inventory"""
    try:
        response = requests.get(f"{API_URL}/export/inventory")
        passed = response.status_code == 200 and 'text/csv' in response.headers.get('content-type', '')
        print_test("GET /export/inventory - Export inventory", passed)
        return passed
    except Exception as e:
        print_test("GET /export/inventory - Export inventory", False)
        print(f"  Error: {e}")
        return False

def test_export_movements():
    """Test exporting movements"""
    try:
        response = requests.get(f"{API_URL}/export/movements")
        passed = response.status_code == 200 and 'text/csv' in response.headers.get('content-type', '')
        print_test("GET /export/movements - Export movements", passed)
        return passed
    except Exception as e:
        print_test("GET /export/movements - Export movements", False)
        print(f"  Error: {e}")
        return False

def test_validation_errors():
    """Test validation errors"""
    print("\n--- Testing Validation ---")
    
    # Test invalid site (missing required fields)
    try:
        response = requests.post(f"{API_URL}/sites/", json={})
        passed = response.status_code == 422
        print_test("Validation: Missing required fields", passed)
    except Exception as e:
        print_test("Validation: Missing required fields", False)
    
    # Test invalid quantity (negative)
    try:
        response = requests.post(f"{API_URL}/inventory/adjust", json={
            "part_id": 1,
            "site_id": 1,
            "quantity": 0,
            "created_by": "Test"
        })
        # Should work with 0, but let's test negative
        response = requests.post(f"{API_URL}/inventory/adjust", json={
            "part_id": 1,
            "site_id": 1,
            "quantity": -1000,
            "created_by": "Test"
        })
        passed = response.status_code in [400, 422]
        print_test("Validation: Insufficient stock", passed)
    except Exception as e:
        print_test("Validation: Insufficient stock", False)

def main():
    print("=" * 60)
    print("🧪 Testing Spare Parts Management System API")
    print("=" * 60)
    print()
    
    # Check if API is running
    if not test_root():
        print("\n❌ API is not running. Please start the backend first:")
        print("   cd backend && uvicorn main:app --reload")
        return
    
    print("\n--- Testing CRUD Operations ---")
    
    # Test Sites
    site_id = test_create_site()
    test_get_sites()
    
    # Test Parts
    part_id = test_create_part()
    test_get_parts()
    test_search_parts()
    
    # Test Inventory
    test_adjust_inventory(site_id, part_id)
    test_get_inventory()
    
    # Test Movements
    test_get_movements()
    
    # Test Requests
    request_id = test_create_request(site_id, part_id)
    test_get_requests()
    test_approve_request(request_id)
    
    # Test Dashboard
    print("\n--- Testing Dashboard ---")
    test_dashboard_summary()
    
    # Test Export
    print("\n--- Testing Export ---")
    test_export_inventory()
    test_export_movements()
    
    # Test Validation
    test_validation_errors()
    
    print("\n" + "=" * 60)
    print("✅ Testing completed!")
    print("=" * 60)
    print("\n💡 Check the results above for any failures")
    print("📚 API Documentation: http://localhost:8000/docs")
    print()

if __name__ == "__main__":
    main()
