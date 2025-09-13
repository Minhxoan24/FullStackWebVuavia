# AccountVuavia Module - Hệ Thống Quản Lý Tài Khoản

## 📋 Tổng quan
Module này quản lý inventory (kho) tài khoản trong hệ thống bán tài khoản. Bao gồm CRUD operations, bulk operations, và logic nghiệp vụ phức tạp.

## 🏗️ Kiến trúc

### Models
- **AccountVuavia**: Model chính lưu trữ thông tin account
- **StatusAccountVuavia**: Enum quản lý trạng thái (AVAILABLE, HOLD, SOLD, EXPIRED)

### Schemas
- **CreateVuaviaSchema**: Tạo account mới 
- **BulkCreateVuaviaSchema**: Tạo nhiều accounts cùng lúc
- **UpdateVuaviaSchema**: Cập nhật account
- **InforAccountVuaviaSchema**: Response thông tin account (không có password)
- **PaginatedAccountVuaviaResponse**: Response có pagination

### Services
- **CreateAccountVuaviaService**: Tạo account với password hash
- **BulkCreateAccountVuaviaService**: Bulk insert tối ưu (1000+ accounts)
- **UpdateAccountVuaviaService**: Update account với validation
- **DeleteAccountVuaviaService**: Xóa account
- **InformationAccountVuaviaService**: List với pagination + filter
- **SelectAccountVuaviaService**: Logic chọn accounts cho order
- **CountAccountVuaviaService**: Đếm accounts theo filter

### Endpoints
```
POST   /account-vuavia/create        - Tạo account mới
POST   /account-vuavia/bulk-create   - Tạo nhiều accounts
GET    /account-vuavia/list          - List accounts (pagination)
GET    /account-vuavia/count         - Đếm accounts
GET    /account-vuavia/stats         - Thống kê tổng quan
PUT    /account-vuavia/update/{id}   - Update account
DELETE /account-vuavia/delete/{id}   - Xóa account
POST   /account-vuavia/sell          - Bán accounts cho customer
```

## 🔐 Bảo mật

### Password Security
- ✅ **Hash passwords**: Dùng bcrypt để hash password trước khi lưu
- ✅ **No password in response**: InforAccountVuaviaSchema không trả password
- ⚠️ **Order password**: Trong CreateOrder, password vẫn được lưu vào JSON (cần review)

### Access Control
- ✅ **Admin only**: Tất cả CRUD operations chỉ admin được dùng
- ✅ **User sell**: Customer chỉ có thể buy/sell, không xem inventory

## 📊 Performance

### Database Indexes
```sql
-- Indexes đã thêm
CREATE INDEX ix_account_vuavia_login_name ON account_vuavia(login_name);
CREATE INDEX ix_account_vuavia_status ON account_vuavia(status);
CREATE INDEX ix_account_vuavia_type_product_id ON account_vuavia(type_product_id);
CREATE INDEX ix_account_vuavia_updated_at ON account_vuavia(updated_at);

-- Composite indexes
CREATE INDEX ix_account_vuavia_status_type ON account_vuavia(status, type_product_id);
CREATE INDEX ix_account_vuavia_hold_timeout ON account_vuavia(status, updated_at);
```

### Optimization Features
- ✅ **Bulk Insert**: `bulk_insert_mappings` cho 1000+ records
- ✅ **Pagination**: Tránh load toàn bộ data
- ✅ **Pessimistic Locking**: `with_for_update` trong SelectAccount
- ✅ **HOLD Timeout**: Auto-release accounts sau 10 phút

## 🔄 Business Logic

### Account Status Flow
```
AVAILABLE → HOLD (khi chọn trong order) → SOLD (khi order hoàn thành)
     ↑          ↓
     └── EXPIRED (timeout 10 phút)
```

### Order Process
1. User tạo order → SelectAccountVuaviaService chọn accounts
2. Accounts được set `HOLD` với timestamp
3. Nếu order thành công → set `SOLD`
4. Nếu order fail/timeout → auto-release về `AVAILABLE`

## 🚀 Usage Examples

### 1. Bulk Create 100 Accounts
```bash
POST /account-vuavia/bulk-create
{
  "accounts": [
    {"login_name": "acc001", "password": "pass123", "type_product_id": 4},
    // ... 99 more
  ]
}
```

### 2. List với Filter + Pagination
```bash
GET /account-vuavia/list?page=1&size=50&status=AVAILABLE&type_product_id=4
```

### 3. Get Statistics
```bash
GET /account-vuavia/stats
# Response: {"AVAILABLE": 950, "HOLD": 20, "SOLD": 30, "TOTAL": 1000}
```

## ⚠️ Known Issues & TODOs

### 🔴 Critical
- [ ] **Order password decryption**: Implement proper password decryption trong order
- [ ] **Rate limiting**: Thêm rate limit cho bulk operations

### 🟡 Medium
- [ ] **Redis caching**: Cache available counts
- [ ] **Background cleanup**: Cron job để cleanup expired accounts
- [ ] **Audit logging**: Log tất cả account operations

### 🟢 Low
- [ ] **Unit tests**: Thêm comprehensive tests
- [ ] **Monitoring**: Metrics cho performance tracking
- [ ] **Documentation**: API docs với OpenAPI

## 🔧 Configuration

### Environment Variables
```env
# Database
DATABASE_URL=postgresql://...

# Security
BCRYPT_ROUNDS=12
ACCOUNT_HOLD_TIMEOUT_MINUTES=10

# Performance
BULK_INSERT_BATCH_SIZE=100
MAX_ACCOUNTS_PER_REQUEST=1000
```

### Alembic Migration
```bash
# Chạy migration để thêm indexes
alembic upgrade head
```

## 🧪 Testing

### Test Commands
```bash
# Unit tests
pytest tests/test_account_vuavia/

# Load test bulk create
locust -f tests/load_test_bulk_create.py

# Integration test
pytest tests/integration/test_account_flow.py
```

---

**Phiên bản**: 2.0.0 (Updated 2025-09-12)  
**Tác giả**: Development Team  
**Status**: ✅ Production Ready (với TODOs)
