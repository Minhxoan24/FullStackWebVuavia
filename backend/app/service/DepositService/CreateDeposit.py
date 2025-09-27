from app.schemas.DepositSchema.CreateDeposit import CreateDepositRequest 
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import DepositRequest, User, TransactionHistory, TransactionType, DepositStatus
from datetime import datetime, timezone
import uuid
import qrcode
from io import BytesIO
import base64
from app.core.config import CASSO_BANK_ACCOUNT_ID, CASSO_BANK_ACCOUNT_NAME, CASSO_CHECKSUM_KEY, CASSO_CLIENT_ID, CASSO_BANK_NAME
import hmac
import hashlib
import json
from fastapi import HTTPException  # Thêm import
from loguru import logger  # Thêm import

async def create_deposit_request(db: AsyncSession, user: User, amount: float) -> dict:
    try:
        if amount <= 0:
            raise ValueError("Amount must be positive")
        
        transaction_code = f"DEP-{uuid.uuid4().hex[:8].upper()}"
        deposit = DepositRequest(user_id=user.id, amount=amount, transaction_code=transaction_code)
        db.add(deposit)
        await db.commit()
        await db.refresh(deposit)
        
        # QR generation - Dùng VietQR API để tạo image URL
        account_clean = CASSO_BANK_ACCOUNT_ID.replace(' ', '')
        qr_code_url = f"https://api.vietqr.io/image/{CASSO_BANK_NAME}-{account_clean}-{int(amount)}-{transaction_code}.png"
        # Không cần tạo QR nữa, trả URL trực tiếp
        
        return {
            "id": deposit.id,
            "amount": deposit.amount,
            "transaction_code": deposit.transaction_code,
            "status": deposit.status.value,
            "qr_code_url": qr_code_url,  # URL image từ VietQR API
            "bank_info": {
                "account": CASSO_BANK_ACCOUNT_ID,
                "name": CASSO_BANK_ACCOUNT_NAME,
                "bank": CASSO_BANK_NAME
            }
        }
    except ValueError as e:
        logger.warning(f"Invalid amount for user {user.id}: {e}")
        raise HTTPException(400, str(e))
    except Exception as e:
        logger.error(f"Error creating deposit for user {user.id}: {e}")
        await db.rollback()  # Rollback nếu commit fail
        raise HTTPException(500, "Internal server error")

def verify_casso_signature(payload: dict, signature: str, secret: str) -> bool:
    try:
        payload_str = json.dumps(payload, separators=(',', ':'), sort_keys=True)
        expected = hmac.new(secret.encode(), payload_str.encode(), hashlib.sha256).hexdigest()
        return hmac.compare_digest(signature, expected)
    except (TypeError, json.JSONDecodeError) as e:
        logger.warning(f"Invalid payload or signature: {e}")
        return False

async def process_deposit_webhook(payload: dict, db: AsyncSession):
    logger.info(f"Received webhook payload: {payload}")  # Thêm log payload
    try:
        signature = payload.get("signature")
        if not signature or not verify_casso_signature(payload, signature, CASSO_CHECKSUM_KEY):
            logger.error("Invalid signature")
            raise HTTPException(400, "Invalid signature")
        
        tid = payload.get("tid")
        amount = payload.get("amount")
        logger.info(f"Processing tid: {tid}, amount: {amount}")  # Thêm log
        if not tid or not amount:
            logger.error("Missing tid or amount")
            raise HTTPException(400, "Missing tid or amount")
        
        deposit = (await db.execute(
            select(DepositRequest).where(DepositRequest.transaction_code == tid, DepositRequest.status == DepositStatus.PENDING)
        )).scalar_one_or_none()
        if not deposit:
            logger.error(f"Deposit not found for tid: {tid}")
            raise HTTPException(404, "Deposit not found")
        
        if abs(deposit.amount - amount) > 0.01:
            logger.error(f"Amount mismatch: expected {deposit.amount}, got {amount}")
            raise HTTPException(400, "Amount mismatch")
        
        user = await db.get(User, deposit.user_id)
        logger.info(f"Updating balance for user {user.id}: +{amount}")
        user.balance += amount
        transaction = TransactionHistory(
            user_id=user.id,
            type=TransactionType.DEPOSIT,
            amount=amount,
            description=f"Nạp tiền từ {payload.get('corresponsiveBankName', 'Ngân hàng')}"
        )
        db.add(transaction)
        deposit.status = DepositStatus.COMPLETED
        deposit.completed_at = datetime.now(timezone.utc).replace(tzinfo=None)
        await db.commit()
        logger.info(f"Deposit completed for user {user.id}, amount {amount}")
    except HTTPException:
        raise  # Re-raise HTTP errors
    except Exception as e:
        logger.error(f"Webhook processing failed: {e}")
        await db.rollback()
        raise HTTPException(500, "Webhook processing failed")

async def check_deposit_status_service(db: AsyncSession, transaction_code: str) -> dict:
    try:
        deposit = (await db.execute(
            select(DepositRequest).where(DepositRequest.transaction_code == transaction_code)
        )).scalar_one_or_none()
        if not deposit:
            raise HTTPException(404, "Deposit not found")
        
        return {
            "transaction_code": deposit.transaction_code,
            "status": deposit.status.value,
            "amount": deposit.amount,
            "created_at": deposit.created_at,
            "completed_at": deposit.completed_at
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Check status failed: {e}")
        raise HTTPException(500, "Failed to check status")
