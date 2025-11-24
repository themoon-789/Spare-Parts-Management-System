const API_URL = 'http://localhost:8000';

// ============ Loading Functions ============
function showLoading() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        overlay.style.display = 'flex';
    }
}

function hideLoading() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        overlay.style.display = 'none';
    }
}

function disableButton(button) {
    if (button) {
        button.disabled = true;
        button.style.opacity = '0.6';
        button.style.cursor = 'not-allowed';
    }
}

function enableButton(button) {
    if (button) {
        button.disabled = false;
        button.style.opacity = '1';
        button.style.cursor = 'pointer';
    }
}

// ============ Utility Functions ============
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 25px;
        border-radius: 8px;
        color: white;
        font-weight: 600;
        z-index: 10000;
        animation: slideIn 0.3s ease-out;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    `;
    
    const colors = {
        success: '#48bb78',
        error: '#f56565',
        warning: '#ed8936',
        info: '#667eea'
    };
    
    alertDiv.style.background = colors[type] || colors.info;
    alertDiv.textContent = message;
    
    document.body.appendChild(alertDiv);
    
    setTimeout(() => {
        alertDiv.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => alertDiv.remove(), 300);
    }, 5000);
}

function switchTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Remove active from all nav tabs
    document.querySelectorAll('.nav-tab').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Show selected tab
    document.getElementById(`${tabName}-tab`).classList.add('active');
    event.target.classList.add('active');
    
    // Load data for the tab
    switch(tabName) {
        case 'dashboard':
            loadDashboard();
            break;
        case 'inventory':
            loadInventory();
            loadSitesForDropdown();
            loadPartsForDropdown();
            break;
        case 'movements':
            loadMovements();
            loadSitesForDropdown();
            break;
        case 'requests':
            loadRequests();
            loadSitesForDropdown();
            loadPartsForDropdown();
            break;
        case 'sites':
            loadSites();
            break;
        case 'parts':
            loadParts();
            break;
    }
}

function formatDate(dateString) {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleDateString('th-TH', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function formatNumber(num) {
    return new Intl.NumberFormat('th-TH').format(num);
}

// ============ Dashboard Functions ============
async function loadDashboard() {
    showLoading();
    try {
        // Load summary
        const summaryRes = await fetch(`${API_URL}/dashboard/summary`);
        if (!summaryRes.ok) {
            throw new Error(`HTTP error! status: ${summaryRes.status}`);
        }
        const summary = await summaryRes.json();
        
        document.getElementById('totalSites').textContent = formatNumber(summary.total_sites);
        document.getElementById('totalParts').textContent = formatNumber(summary.total_parts);
        document.getElementById('lowStock').textContent = formatNumber(summary.low_stock_items);
        document.getElementById('pendingRequests').textContent = formatNumber(summary.pending_requests);
        
        // Load low stock items
        const lowStockRes = await fetch(`${API_URL}/inventory/?low_stock=true`);
        const lowStockItems = await lowStockRes.json();
        
        const lowStockTable = document.getElementById('lowStockTable');
        lowStockTable.innerHTML = '';
        
        if (lowStockItems.length === 0) {
            lowStockTable.innerHTML = '<tr><td colspan="5" class="empty-state">ไม่มีสต็อกต่ำ</td></tr>';
        } else {
            lowStockItems.forEach(item => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${item.site_code} - ${item.site_name}</td>
                    <td>${item.part_number}</td>
                    <td>${item.part_name}</td>
                    <td>${formatNumber(item.quantity)}</td>
                    <td>${formatNumber(item.min_stock_level)}</td>
                `;
                lowStockTable.appendChild(row);
            });
        }
        
        // Load pending requests
        const pendingRes = await fetch(`${API_URL}/requests/?status=pending`);
        const pendingReqs = await pendingRes.json();
        
        const pendingTable = document.getElementById('pendingRequestsTable');
        pendingTable.innerHTML = '';
        
        if (pendingReqs.length === 0) {
            pendingTable.innerHTML = '<tr><td colspan="6" class="empty-state">ไม่มีคำขอรออนุมัติ</td></tr>';
        } else {
            pendingReqs.forEach(req => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${req.site_code} - ${req.site_name}</td>
                    <td>${req.part_number} - ${req.part_name}</td>
                    <td>${formatNumber(req.quantity)}</td>
                    <td>${req.requested_by}</td>
                    <td>${formatDate(req.request_date)}</td>
                    <td>
                        <button class="btn btn-success btn-sm" onclick="approveRequest(${req.id})">อนุมัติ</button>
                        <button class="btn btn-danger btn-sm" onclick="rejectRequest(${req.id})">ปฏิเสธ</button>
                    </td>
                `;
                pendingTable.appendChild(row);
            });
        }
        
    } catch (error) {
        console.error('Error loading dashboard:', error);
        showAlert('ไม่สามารถโหลดข้อมูล Dashboard ได้', 'error');
    } finally {
        hideLoading();
    }
}

async function approveRequest(requestId) {
    const approvedBy = prompt('ชื่อผู้อนุมัติ:');
    if (!approvedBy) return;
    
    try {
        const response = await fetch(`${API_URL}/requests/${requestId}/approve`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ approved_by: approvedBy })
        });
        
        if (response.ok) {
            showAlert('อนุมัติคำขอสำเร็จ', 'success');
            loadDashboard();
        } else {
            const error = await response.json();
            showAlert(error.detail || 'เกิดข้อผิดพลาด', 'error');
        }
    } catch (error) {
        console.error('Error approving request:', error);
        showAlert('ไม่สามารถอนุมัติคำขอได้', 'error');
    }
}

async function rejectRequest(requestId) {
    const approvedBy = prompt('ชื่อผู้ปฏิเสธ:');
    if (!approvedBy) return;
    
    const rejectReason = prompt('เหตุผลในการปฏิเสธ:');
    if (!rejectReason) return;
    
    try {
        const response = await fetch(`${API_URL}/requests/${requestId}/reject`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                approved_by: approvedBy,
                reject_reason: rejectReason
            })
        });
        
        if (response.ok) {
            showAlert('ปฏิเสธคำขอสำเร็จ', 'success');
            loadDashboard();
        } else {
            const error = await response.json();
            showAlert(error.detail || 'เกิดข้อผิดพลาด', 'error');
        }
    } catch (error) {
        console.error('Error rejecting request:', error);
        showAlert('ไม่สามารถปฏิเสธคำขอได้', 'error');
    }
}

// ============ Inventory Functions ============
async function loadInventory() {
    const siteId = document.getElementById('inventorySiteFilter').value;
    const url = siteId ? `${API_URL}/inventory/?site_id=${siteId}` : `${API_URL}/inventory/`;
    
    try {
        const response = await fetch(url);
        const inventory = await response.json();
        
        const table = document.getElementById('inventoryTable');
        table.innerHTML = '';
        
        if (inventory.length === 0) {
            table.innerHTML = '<tr><td colspan="8" class="empty-state">ไม่มีข้อมูล</td></tr>';
        } else {
            inventory.forEach(item => {
                const row = document.createElement('tr');
                
                // Highlight low stock items
                const isLowStock = item.quantity < item.min_stock_level;
                if (isLowStock) {
                    row.style.backgroundColor = '#fef5e7';
                }
                
                row.innerHTML = `
                    <td>${item.site_code} - ${item.site_name}</td>
                    <td>${item.part_number}</td>
                    <td>${item.part_name}</td>
                    <td>${item.location || '-'}</td>
                    <td>${item.ios_version || '-'}</td>
                    <td>${formatNumber(item.quantity)}</td>
                    <td>${formatNumber(item.min_stock_level)}</td>
                    <td>${formatDate(item.last_updated)}</td>
                `;
                table.appendChild(row);
            });
        }
    } catch (error) {
        console.error('Error loading inventory:', error);
        showAlert('ไม่สามารถโหลดข้อมูล Inventory ได้', 'error');
    }
}

function showAdjustForm() {
    const form = document.getElementById('inventoryForm');
    form.classList.add('active');
}

function hideAdjustForm() {
    const form = document.getElementById('inventoryForm');
    form.classList.remove('active');
}

function toggleInventoryForm() {
    const form = document.getElementById('inventoryForm');
    form.classList.toggle('active');
}

async function adjustInventory(e) {
    if (e) e.preventDefault();
    
    const data = {
        part_id: parseInt(document.getElementById('invPart').value),
        site_id: parseInt(document.getElementById('invSite').value),
        quantity: parseInt(document.getElementById('invQuantity').value),
        created_by: document.getElementById('invCreatedBy').value,
        remark: document.getElementById('invRemark').value
    };
    
    if (!data.part_id || !data.site_id || !data.created_by) {
        showAlert('กรุณากรอกข้อมูลให้ครบถ้วน', 'warning');
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/inventory/adjust`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            showAlert('ปรับปรุงสต็อกสำเร็จ', 'success');
            hideAdjustForm();
            loadInventory();
            // Clear form
            document.getElementById('invQuantity').value = '';
            document.getElementById('invCreatedBy').value = '';
            document.getElementById('invRemark').value = '';
        } else {
            const error = await response.json();
            showAlert(error.detail || 'เกิดข้อผิดพลาด', 'error');
        }
    } catch (error) {
        console.error('Error adjusting inventory:', error);
        showAlert('ไม่สามารถปรับปรุงสต็อกได้', 'error');
    }
}

async function submitInventoryAdjust() {
    await adjustInventory();
}

function exportInventory() {
    const siteId = document.getElementById('inventorySiteFilter').value;
    const url = siteId ? `${API_URL}/export/inventory?site_id=${siteId}` : `${API_URL}/export/inventory`;
    window.open(url, '_blank');
}

// ============ Movements Functions ============
function getMovementTypeBadge(type) {
    const badges = {
        purchase: '<span class="badge" style="background: #e6f7ed; color: #48bb78;">ซื้อเข้า</span>',
        transfer: '<span class="badge" style="background: #e6f2ff; color: #667eea;">โอนย้าย</span>',
        issue: '<span class="badge" style="background: #fef5e7; color: #ed8936;">เบิกใช้</span>',
        return: '<span class="badge" style="background: #e6f7ed; color: #48bb78;">คืนสต็อก</span>',
        adjust: '<span class="badge" style="background: #e6f2ff; color: #667eea;">ปรับปรุง</span>'
    };
    return badges[type] || `<span class="badge">${type}</span>`;
}

async function loadMovements() {
    const siteId = document.getElementById('movementSiteFilter').value;
    const type = document.getElementById('movementTypeFilter').value;
    
    let url = `${API_URL}/movements/?`;
    if (siteId) url += `site_id=${siteId}&`;
    if (type) url += `movement_type=${type}&`;
    
    try {
        const response = await fetch(url);
        const movements = await response.json();
        
        const table = document.getElementById('movementsTable');
        table.innerHTML = '';
        
        if (movements.length === 0) {
            table.innerHTML = '<tr><td colspan="9" class="empty-state">ไม่มีข้อมูล</td></tr>';
        } else {
            movements.forEach(mov => {
                const fromSite = mov.from_site_code ? `${mov.from_site_code} - ${mov.from_site_name}` : '-';
                const toSite = mov.to_site_code ? `${mov.to_site_code} - ${mov.to_site_name}` : '-';
                
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${formatDate(mov.created_at)}</td>
                    <td>${mov.part_number} - ${mov.part_name}</td>
                    <td>${fromSite}</td>
                    <td>${toSite}</td>
                    <td>${formatNumber(mov.quantity)}</td>
                    <td>${getMovementTypeBadge(mov.movement_type)}</td>
                    <td>${mov.reference_no || '-'}</td>
                    <td>${mov.created_by || '-'}</td>
                `;
                table.appendChild(row);
            });
        }
    } catch (error) {
        console.error('Error loading movements:', error);
        showAlert('ไม่สามารถโหลดข้อมูล Movements ได้', 'error');
    }
}

function exportMovements() {
    const siteId = document.getElementById('movementSiteFilter').value;
    let url = `${API_URL}/export/movements`;
    if (siteId) url += `?site_id=${siteId}`;
    window.open(url, '_blank');
}

// ============ Requests Functions ============
function getStatusBadge(status) {
    const badges = {
        pending: '<span class="badge badge-pending">รออนุมัติ</span>',
        approved: '<span class="badge badge-approved">อนุมัติแล้ว</span>',
        rejected: '<span class="badge badge-rejected">ปฏิเสธ</span>'
    };
    return badges[status] || `<span class="badge">${status}</span>`;
}

async function loadRequests() {
    const status = document.getElementById('requestStatusFilter').value;
    const url = status ? `${API_URL}/requests/?status=${status}` : `${API_URL}/requests/`;
    
    try {
        const response = await fetch(url);
        const requests = await response.json();
        
        const table = document.getElementById('requestsTable');
        table.innerHTML = '';
        
        if (requests.length === 0) {
            table.innerHTML = '<tr><td colspan="8" class="empty-state">ไม่มีข้อมูล</td></tr>';
        } else {
            requests.forEach(req => {
                const actions = req.status === 'pending' 
                    ? `<button class="btn btn-success btn-sm" onclick="approveRequest(${req.id})">อนุมัติ</button>
                       <button class="btn btn-danger btn-sm" onclick="rejectRequest(${req.id})">ปฏิเสธ</button>`
                    : '-';
                
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${req.site_code} - ${req.site_name}</td>
                    <td>${req.part_number} - ${req.part_name}</td>
                    <td>${formatNumber(req.quantity)}</td>
                    <td>${req.requested_by}</td>
                    <td>${formatDate(req.request_date)}</td>
                    <td>${getStatusBadge(req.status)}</td>
                    <td>${req.approved_by || '-'}</td>
                    <td>${actions}</td>
                `;
                table.appendChild(row);
            });
        }
    } catch (error) {
        console.error('Error loading requests:', error);
        showAlert('ไม่สามารถโหลดข้อมูล Requests ได้', 'error');
    }
}

function showRequestForm() {
    const form = document.getElementById('requestForm');
    form.classList.add('active');
}

function hideRequestForm() {
    const form = document.getElementById('requestForm');
    form.classList.remove('active');
}

function toggleRequestForm() {
    const form = document.getElementById('requestForm');
    form.classList.toggle('active');
}

async function createRequest(e) {
    if (e) e.preventDefault();
    
    const data = {
        site_id: parseInt(document.getElementById('reqSite').value),
        part_id: parseInt(document.getElementById('reqPart').value),
        quantity: parseInt(document.getElementById('reqQuantity').value),
        requested_by: document.getElementById('reqRequestedBy').value,
        remark: document.getElementById('reqRemark').value
    };
    
    if (!data.site_id || !data.part_id || !data.quantity || !data.requested_by) {
        showAlert('กรุณากรอกข้อมูลให้ครบถ้วน', 'warning');
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/requests/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            showAlert('สร้างคำขอสำเร็จ', 'success');
            hideRequestForm();
            loadRequests();
            // Clear form
            document.getElementById('reqQuantity').value = '';
            document.getElementById('reqRequestedBy').value = '';
            document.getElementById('reqRemark').value = '';
        } else {
            const error = await response.json();
            showAlert(error.detail || 'เกิดข้อผิดพลาด', 'error');
        }
    } catch (error) {
        console.error('Error creating request:', error);
        showAlert('ไม่สามารถสร้างคำขอได้', 'error');
    }
}

async function submitRequest() {
    await createRequest();
}

// Custom Modal for Approve/Reject
function createApprovalModal(requestId, isApprove) {
    const approvers = ['siraphop', 'Decho', 'Tin', 'Kriangkrai', 'Veerapot', 'Arom'];
    
    const modalHTML = `
        <div id="approvalModal" style="
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 10000;
        ">
            <div style="
                background: white;
                padding: 30px;
                border-radius: 15px;
                max-width: 500px;
                width: 90%;
                box-shadow: 0 10px 40px rgba(0,0,0,0.3);
            ">
                <h3 style="margin-bottom: 20px; color: #2d3748;">
                    ${isApprove ? '✅ อนุมัติคำขอ' : '❌ ปฏิเสธคำขอ'}
                </h3>
                
                <div style="margin-bottom: 15px;">
                    <label style="display: block; margin-bottom: 8px; font-weight: 600; color: #2d3748;">
                        ${isApprove ? 'ผู้อนุมัติ' : 'ผู้ปฏิเสธ'} *
                    </label>
                    <select id="approverSelect" style="
                        width: 100%;
                        padding: 10px;
                        border: 2px solid #e2e8f0;
                        border-radius: 8px;
                        font-size: 14px;
                    ">
                        <option value="">เลือก...</option>
                        ${approvers.map(name => `<option value="${name}">${name}</option>`).join('')}
                    </select>
                </div>
                
                ${!isApprove ? `
                    <div style="margin-bottom: 15px;">
                        <label style="display: block; margin-bottom: 8px; font-weight: 600; color: #2d3748;">
                            เหตุผลในการปฏิเสธ *
                        </label>
                        <textarea id="rejectReason" rows="3" style="
                            width: 100%;
                            padding: 10px;
                            border: 2px solid #e2e8f0;
                            border-radius: 8px;
                            font-size: 14px;
                            resize: vertical;
                        "></textarea>
                    </div>
                ` : ''}
                
                <div style="display: flex; gap: 10px; justify-content: flex-end; margin-top: 20px;">
                    <button onclick="closeApprovalModal()" class="btn btn-danger">
                        ยกเลิก
                    </button>
                    <button onclick="submitApproval(${requestId}, ${isApprove})" class="btn ${isApprove ? 'btn-success' : 'btn-danger'}">
                        ${isApprove ? 'อนุมัติ' : 'ปฏิเสธ'}
                    </button>
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHTML);
}

function closeApprovalModal() {
    const modal = document.getElementById('approvalModal');
    if (modal) modal.remove();
}

async function submitApproval(requestId, isApprove) {
    const approvedBy = document.getElementById('approverSelect').value;
    
    if (!approvedBy) {
        showAlert('กรุณาเลือกผู้' + (isApprove ? 'อนุมัติ' : 'ปฏิเสธ'), 'warning');
        return;
    }
    
    let data = { approved_by: approvedBy };
    
    if (!isApprove) {
        const rejectReason = document.getElementById('rejectReason').value.trim();
        if (!rejectReason) {
            showAlert('กรุณาระบุเหตุผลในการปฏิเสธ', 'warning');
            return;
        }
        data.reject_reason = rejectReason;
    }
    
    try {
        const endpoint = isApprove ? 'approve' : 'reject';
        const response = await fetch(`${API_URL}/requests/${requestId}/${endpoint}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            showAlert((isApprove ? 'อนุมัติ' : 'ปฏิเสธ') + 'คำขอสำเร็จ', 'success');
            closeApprovalModal();
            loadRequests();
            loadDashboard(); // Refresh dashboard
        } else {
            const error = await response.json();
            showAlert(error.detail || 'เกิดข้อผิดพลาด', 'error');
        }
    } catch (error) {
        console.error('Error processing request:', error);
        showAlert('ไม่สามารถดำเนินการได้', 'error');
    }
}

function approveRequest(requestId) {
    createApprovalModal(requestId, true);
}

function rejectRequest(requestId) {
    createApprovalModal(requestId, false);
}

// ============ Sites Functions ============
async function loadSites() {
    try {
        const response = await fetch(`${API_URL}/sites/`);
        const sites = await response.json();
        
        const table = document.getElementById('sitesTable');
        table.innerHTML = '';
        
        if (sites.length === 0) {
            table.innerHTML = '<tr><td colspan="5" class="empty-state">ไม่มีข้อมูล</td></tr>';
        } else {
            sites.forEach(site => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${site.site_code}</td>
                    <td>${site.site_name}</td>
                    <td>${site.province || '-'}</td>
                    <td>${site.contact_person || '-'}</td>
                    <td>${site.phone || '-'}</td>
                `;
                table.appendChild(row);
            });
        }
    } catch (error) {
        console.error('Error loading sites:', error);
        showAlert('ไม่สามารถโหลดข้อมูล Sites ได้', 'error');
    }
}

function toggleSiteForm() {
    const form = document.getElementById('siteForm');
    form.classList.toggle('active');
}

async function submitSite() {
    const data = {
        site_code: document.getElementById('siteCode').value,
        site_name: document.getElementById('siteName').value,
        province: document.getElementById('siteProvince').value,
        address: document.getElementById('siteAddress').value,
        contact_person: document.getElementById('siteContact').value,
        phone: document.getElementById('sitePhone').value
    };
    
    if (!data.site_code || !data.site_name) {
        showAlert('กรุณากรอกรหัสศูนย์และชื่อศูนย์', 'warning');
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/sites/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            showAlert('เพิ่มศูนย์สำเร็จ', 'success');
            toggleSiteForm();
            loadSites();
            // Clear form
            document.getElementById('siteCode').value = '';
            document.getElementById('siteName').value = '';
            document.getElementById('siteProvince').value = '';
            document.getElementById('siteAddress').value = '';
            document.getElementById('siteContact').value = '';
            document.getElementById('sitePhone').value = '';
        } else {
            const error = await response.json();
            showAlert(error.detail || 'เกิดข้อผิดพลาด', 'error');
        }
    } catch (error) {
        console.error('Error creating site:', error);
        showAlert('ไม่สามารถเพิ่มศูนย์ได้', 'error');
    }
}

// ============ Parts Functions ============
async function loadParts() {
    try {
        const response = await fetch(`${API_URL}/parts/`);
        const parts = await response.json();
        
        const table = document.getElementById('partsTable');
        table.innerHTML = '';
        
        if (parts.length === 0) {
            table.innerHTML = '<tr><td colspan="8" class="empty-state">ไม่มีข้อมูล</td></tr>';
        } else {
            parts.forEach(part => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${part.part_number}</td>
                    <td>${part.part_name}</td>
                    <td>${part.brand || '-'}</td>
                    <td>${part.model || '-'}</td>
                    <td>${part.location || '-'}</td>
                    <td>${part.ios_version || '-'}</td>
                    <td>${part.unit}</td>
                    <td>${formatNumber(part.min_stock_level)}</td>
                `;
                table.appendChild(row);
            });
        }
    } catch (error) {
        console.error('Error loading parts:', error);
        showAlert('ไม่สามารถโหลดข้อมูล Parts ได้', 'error');
    }
}

function togglePartForm() {
    const form = document.getElementById('partForm');
    form.classList.toggle('active');
}

async function submitPart() {
    const data = {
        part_number: document.getElementById('partNumber').value,
        part_name: document.getElementById('partName').value,
        category: document.getElementById('partCategory').value,
        brand: document.getElementById('partBrand').value,
        model: document.getElementById('partModel').value,
        location: document.getElementById('partLocation').value,
        ios_version: document.getElementById('partIosVersion').value,
        unit: document.getElementById('partUnit').value || 'pcs',
        min_stock_level: parseInt(document.getElementById('partMinStock').value) || 5,
        description: document.getElementById('partDescription').value
    };
    
    if (!data.part_number || !data.part_name) {
        showAlert('กรุณากรอก Part Number และชื่ออะไหล่', 'warning');
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/parts/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            showAlert('เพิ่มอะไหล่สำเร็จ', 'success');
            togglePartForm();
            loadParts();
            // Clear form
            document.getElementById('partNumber').value = '';
            document.getElementById('partName').value = '';
            document.getElementById('partCategory').value = '';
            document.getElementById('partBrand').value = '';
            document.getElementById('partModel').value = '';
            document.getElementById('partLocation').value = '';
            document.getElementById('partIosVersion').value = '';
            document.getElementById('partUnit').value = 'pcs';
            document.getElementById('partMinStock').value = '5';
            document.getElementById('partDescription').value = '';
        } else {
            const error = await response.json();
            showAlert(error.detail || 'เกิดข้อผิดพลาด', 'error');
        }
    } catch (error) {
        console.error('Error creating part:', error);
        showAlert('ไม่สามารถเพิ่มอะไหล่ได้', 'error');
    }
}

// ============ Dropdown Loaders ============
async function loadSitesForDropdown() {
    try {
        const response = await fetch(`${API_URL}/sites/`);
        const sites = await response.json();
        
        // Update all site dropdowns
        const dropdowns = ['inventorySiteFilter', 'movementSiteFilter', 'invSite', 'reqSite'];
        dropdowns.forEach(id => {
            const select = document.getElementById(id);
            if (select) {
                const currentValue = select.value;
                const isFilter = id.includes('Filter');
                
                select.innerHTML = isFilter ? '<option value="">ทุกศูนย์</option>' : '<option value="">เลือกศูนย์</option>';
                
                sites.forEach(site => {
                    const option = document.createElement('option');
                    option.value = site.id;
                    option.textContent = `${site.site_code} - ${site.site_name}`;
                    select.appendChild(option);
                });
                
                if (currentValue) select.value = currentValue;
            }
        });
    } catch (error) {
        console.error('Error loading sites for dropdown:', error);
    }
}

async function loadPartsForDropdown() {
    try {
        const response = await fetch(`${API_URL}/parts/`);
        const parts = await response.json();
        
        // Update all part dropdowns
        const dropdowns = ['invPart', 'reqPart'];
        dropdowns.forEach(id => {
            const select = document.getElementById(id);
            if (select) {
                select.innerHTML = '<option value="">เลือกอะไหล่</option>';
                
                parts.forEach(part => {
                    const option = document.createElement('option');
                    option.value = part.id;
                    option.textContent = `${part.part_number} - ${part.part_name}`;
                    select.appendChild(option);
                });
            }
        });
    } catch (error) {
        console.error('Error loading parts for dropdown:', error);
    }
}

// ============ Initialize ============
document.addEventListener('DOMContentLoaded', async () => {
    try {
        await loadSites();
        await loadParts();
        await loadSitesForDropdown();
        await loadPartsForDropdown();
        await loadDashboard();
    } catch (error) {
        console.error('Error during initialization:', error);
        showAlert('เกิดข้อผิดพลาดในการโหลดข้อมูลเริ่มต้น', 'error');
    }
});
