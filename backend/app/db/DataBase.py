# Import các class cần thiết từ SQLAlchemy async
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
# Import cấu hình database từ file config
from app.core.config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME 

# Tạo chuỗi kết nối database với format PostgreSQL + asyncpg driver
# Format: postgresql+asyncpg://username:password@host:port/database_name
DATA_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Tạo engine - công cụ kết nối và quản lý database
# echo=True: in ra các câu lệnh SQL được thực thi (để debug)
# future=True: sử dụng API mới của SQLAlchemy 2.0
engine = create_async_engine(DATA_URL, echo=True, future=True , pool_size=20,           # Thêm sau
    max_overflow=30)  # Tối đa 50 kết nối (20 + 30 overflow) , pool_size=20: giữ sẵn 20 kết nối trong pool , max_overflow=30: có thể tạo thêm 30 kết nối 

# Tạo factory để tạo các session database (phiên làm việc với DB)
# bind=engine: liên kết với engine đã tạo ở trên
# class_=AsyncSession: sử dụng AsyncSession cho async operations
# expire_on_commit=False: không làm expire objects sau khi commit (an toàn hơn)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,                    # Liên kết với database engine
    class_=AsyncSession,           # Sử dụng AsyncSession class
    expire_on_commit=False         # Không expire objects sau commit
) 

# Tạo session factory thứ hai với cùng cấu hình
# Có thể dùng cho các trường hợp đặc biệt hoặc tách biệt logic
StrictSessionLocal = async_sessionmaker(
    bind=engine,                    # Liên kết với database engine
    class_=AsyncSession,           # Sử dụng AsyncSession class
    expire_on_commit=False         # Không expire objects sau commit
)

# Dependency function cho FastAPI - cung cấp database session
# Được inject vào các endpoint thông qua Depends()
async def get_async_session():
    # Tạo session từ factory và sử dụng async context manager
    async with AsyncSessionLocal() as session:
        try:
            # Yield session để FastAPI có thể inject vào endpoint , Yield cho phép sử dụng session trong các endpoint
            yield session
        except Exception:
            # Nếu có lỗi xảy ra, rollback tất cả changes chưa commit
            await session.rollback()  
            # Re-raise exception để FastAPI xử lý
            raise
        
# Dependency function thứ hai sử dụng StrictSessionLocal
# Logic tương tự như get_async_session()
async def get_strict_session(): 
    # Tạo session từ StrictSessionLocal factory
    async with StrictSessionLocal() as session:
        try:
            # Yield session cho FastAPI dependency injection
            yield session
        except Exception:
            # Rollback changes nếu có exception
            await session.rollback()
            # Re-raise exception để caller xử lý
            raise