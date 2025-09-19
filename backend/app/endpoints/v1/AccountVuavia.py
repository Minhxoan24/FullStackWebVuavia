from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.db.DataBase import get_async_session
from app.core.auth import get_current_user
from app.core.author import get_current_admin_user
from app.models.Users import User

# Schema imports
from app.schemas.AccountVuaviaSchema.CreateVuavia import CreateVuaviaSchema, BulkCreateVuaviaSchema
from app.schemas.AccountVuaviaSchema.UpdateVuavia import UpdateVuaviaSchema
from app.schemas.AccountVuaviaSchema.DeleteVuavia import DeleteVuaviaSchema
from app.schemas.AccountVuaviaSchema.InforAccountVuaviaSchema import InforAccountVuaviaSchema
from app.schemas.AccountVuaviaSchema.PaginatedAccountResponse import PaginatedAccountVuaviaResponse
from app.schemas.AccountVuaviaSchema.SellAccountSchema import SellAccountRequestSchema, AccountSelectionSchema  # Thêm import
from app.schemas.Message.Message import MessageSchema

# Service imports
from app.service.AccountVuavias.CreatAccountVuavia import CreateAccountVuaviaService
from app.service.AccountVuavias.BulkCreateAccountVuavia import BulkCreateAccountVuaviaService  # Thêm import
from app.service.AccountVuavias.UpdateAccountVuavia import UpdateAccountVuaviaService
from app.service.AccountVuavias.DeleteAccountVuavia import DeleteAccountVuaviaService
from app.service.AccountVuavias.InformationAccountVuavia import InformationAccountVuaviaService
from app.service.AccountVuavias.SellAccountService import SellAccountService, GetAvailableCountByType  # Thêm import
from app.service.AccountVuavias.CountAccount import CountAccountVuaviaService, GetAccountStatsService

router = APIRouter(tags=["AccountVuavia"], prefix="/account-vuavia")

@router.post("/create", response_model=MessageSchema)
async def create_account_vuavia(
    account_vuavia: CreateVuaviaSchema,
    db: AsyncSession = Depends(get_async_session),
    # admin_user: User = Depends(get_current_admin_user)  # Chỉ admin mới được thêm
):
    """Thêm tài khoản mới vào kho tài khoản Vuavia"""
    return await CreateAccountVuaviaService(account_vuavia, db)

@router.post("/bulk-create", response_model=MessageSchema)
async def bulk_create_account_vuavia(
    bulk_accounts: BulkCreateVuaviaSchema,
    db: AsyncSession = Depends(get_async_session),
    admin_user: User = Depends(get_current_admin_user)
):
    """Thêm nhiều tài khoản mới vào kho (bulk insert)"""
    return await BulkCreateAccountVuaviaService(bulk_accounts, db)

@router.get("/list", response_model=PaginatedAccountVuaviaResponse)
async def list_account_vuavia(
    page: int = Query(1, ge=1, description="Page number (1-based)"),
    size: int = Query(50, ge=1, le=100, description="Page size (max 100)"),
    status: Optional[str] = Query(None, description="Filter by status: AVAILABLE, HOLD, SOLD, EXPIRED"),
    type_product_id: Optional[int] = Query(None, description="Filter by type product ID"),
    db: AsyncSession = Depends(get_async_session),
    admin_user: User = Depends(get_current_admin_user)
):
    """Lấy danh sách tài khoản với pagination và filter"""
    from app.service.AccountVuavias.InformationAccountVuavia import InformationAccountVuaviaService
    
    result = await InformationAccountVuaviaService(db, page, size, status, type_product_id)
    
    return PaginatedAccountVuaviaResponse(
        accounts=result.accounts,
        total=result.total,
        page=result.page,
        size=result.size,
        total_pages=result.total_pages
    )

@router.get("/count")
async def count_account_vuavia(
    type_product_id: Optional[int] = Query(None, description="Type product ID to count"),
    db: AsyncSession = Depends(get_async_session),
    admin_user: User = Depends(get_current_admin_user)
):
    """Đếm số lượng tài khoản AVAILABLE trong kho"""
    count = await CountAccountVuaviaService(type_product_id, db)
    return {"available_count": count, "type_product_id": type_product_id}

@router.get("/stats")
async def get_account_stats(
    db: AsyncSession = Depends(get_async_session),
    admin_user: User = Depends(get_current_admin_user)
):
    """Lấy thống kê tổng quan về accounts"""
    return await GetAccountStatsService(db)



@router.put("/update/{account_id}", response_model=MessageSchema)  # Thêm {account_id}
async def update_account_vuavia(
    account_id: int,  # Path param
    account_update: UpdateVuaviaSchema,  # Body chỉ chứa fields update
    db: AsyncSession = Depends(get_async_session),
    admin_user: User = Depends(get_current_admin_user)
):
    """Cập nhật thông tin tài khoản trong kho"""
    # Truyền account_id vào service thay vì dùng từ body
    return await UpdateAccountVuaviaService(account_id, account_update, db)

@router.delete("/delete/{account_id}", response_model=MessageSchema)  # Thêm {account_id}
async def delete_account_vuavia(
    account_id: int,  # Path param
    db: AsyncSession = Depends(get_async_session),
    admin_user: User = Depends(get_current_admin_user)
):
    """Xóa tài khoản khỏi kho"""
    return await DeleteAccountVuaviaService(account_id, db)  # Truyền account_id

@router.post("/sell", response_model=list[AccountSelectionSchema])
async def sell_accounts(
    sell_request: SellAccountRequestSchema,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)  # User thường có thể mua
):
    """Bán accounts cho customer - assign accounts từ inventory"""
    return await SellAccountService(sell_request, db)

@router.get("/available-count/{type_product_id}")
async def get_available_count(
    type_product_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    """Đếm số accounts AVAILABLE theo type product"""
    count = await GetAvailableCountByType(type_product_id, db)
    return {"type_product_id": type_product_id, "available_count": count}