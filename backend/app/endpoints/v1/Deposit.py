from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.DataBase import get_async_session
from app.core.auth import get_current_user
from app.models.Users import User
from app.schemas.DepositSchema.CreateDeposit import CreateDepositRequest
from app.service.DepositService.CreateDeposit import create_deposit_request, process_deposit_webhook, check_deposit_status_service
from loguru import logger

router = APIRouter(tags=["Deposit"], prefix="/deposit")

@router.post("/create")
async def create_deposit(
    data: CreateDepositRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
   
    return await create_deposit_request(db, user, data.amount)
    
@router.post("/webhook")
async def deposit_webhook(
    payload: dict,
    db: AsyncSession = Depends(get_async_session)
):
    
    return await process_deposit_webhook(payload, db)

@router.get("/status/{transaction_code}")
async def check_deposit_status(
    transaction_code: str,
    db: AsyncSession = Depends(get_async_session)
):
    return await check_deposit_status_service(db, transaction_code)
