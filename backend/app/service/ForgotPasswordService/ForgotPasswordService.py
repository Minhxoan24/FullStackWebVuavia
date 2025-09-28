from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone
import random
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.models.Users import User
from app.Utils.HashPassword import hash_password
from app.service.RedisService.RedisService import redis_service
from app.service.EmailService.EmailService import email_service
from app.schemas.Message.Message import MessageSchema as Message

# Cấu hình logging
logger = logging.getLogger(__name__)

# Constants
MAX_SEND_PER_DAY = 7
OTP_TTL_SECONDS = 180  # 3 minutes
MAX_ATTEMPTS = 5       # Maximum OTP attempts
OTP_LENGTH = 6         # OTP length

def _generate_otp(length: int = OTP_LENGTH) -> str:
    """Generate secure OTP with specified length"""
    return ''.join(random.choices('0123456789', k=length))

def _validate_email_format(email: str) -> bool:
    """Basic email validation"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def _validate_password_strength(password: str) -> tuple[bool, str]:
    """Validate password strength"""
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    if len(password) > 128:
        return False, "Password must be at most 128 characters long"
    
    # Optional: Add more strength checks
    # if not re.search(r'[A-Z]', password):
    #     return False, "Password must contain at least one uppercase letter"
    
    return True, "Password is valid"

async def request_password_reset_otp(email: str, db: AsyncSession) -> Message:
    """
    Request OTP for password reset
    
    Args:
        email: User email address
        db: Database session
        
    Returns:
        Message: Response with status and message
        
    Raises:
        HTTPException: Various HTTP exceptions for different scenarios
    """
    try:
        # Validate email format
        if not _validate_email_format(email):
            raise HTTPException(status_code=400, detail="Định dạng email không hợp lệ")

        # Normalize email (lowercase, strip)
        email = email.lower().strip()

        # Check if user exists
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()

        # Security: Don't reveal if user exists or not
        if not user:
            logger.warning(f"Password reset requested for non-existent email: {email}")
            # Still return success to prevent email enumeration
            return Message(status="success", message="Nếu email tồn tại, mã OTP đã được gửi")

        # Check daily rate limit
        current_count = await redis_service.get_daily_send_count(email)
        if current_count >= MAX_SEND_PER_DAY:
            logger.warning(f"Daily OTP limit exceeded for email: {email}")
            raise HTTPException(
                status_code=429,
                detail=f"Đã đạt giới hạn gửi mã trong ngày ({MAX_SEND_PER_DAY}). Vui lòng thử lại vào ngày mai."
            )

        # Generate and store OTP
        otp = _generate_otp(OTP_LENGTH)
        await redis_service.set_otp(email, otp, ttl_seconds=OTP_TTL_SECONDS)

        # Increment daily counter
        await redis_service.increment_daily_send(email)

        # Send email asynchronously
        try:
            await email_service.send_otp_email(email, otp)
            logger.info(f"OTP sent successfully to: {email}")
        except Exception as e:
            logger.error(f"Failed to send OTP email to {email}: {str(e)}")
            # Đừng trả lỗi cho client để tránh lộ thông tin; chỉ log để debug.

        return Message(status="success", message="OTP đã được gửi")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in request_password_reset_otp: {str(e)}")
        try:
            await db.rollback()
        except Exception:
            # ignore rollback errors
            pass
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

async def verify_password_reset_otp(email: str, otp: str) -> Message:
    """
    Verify OTP for password reset
    
    Args:
        email: User email address  
        otp: OTP code to verify
        
    Returns:
        Message: Response with status and message
        
    Raises:
        HTTPException: Various HTTP exceptions for different scenarios
    """
    try:
        # Validate inputs
        if not _validate_email_format(email):
            raise HTTPException(status_code=400, detail="Định dạng email không hợp lệ")

        if not otp or len(otp.strip()) != OTP_LENGTH:
            raise HTTPException(status_code=400, detail=f"Mã OTP phải gồm đúng {OTP_LENGTH} chữ số")

        # Normalize inputs
        email = email.lower().strip()
        otp = otp.strip()

        # Get OTP data from Redis
        data = await redis_service.get_otp(email)
        if not data:
            # Try to provide a clearer message: check TTL if possible
            try:
                ttl = await redis_service.get_otp_ttl(email)
            except Exception:
                ttl = None

            if ttl == -2:
                # Key does not exist (never created or already deleted)
                msg = "Không tìm thấy mã OTP. Vui lòng yêu cầu mã mới."
            elif isinstance(ttl, int) and ttl <= 0:
                # Key existed but TTL elapsed (best-effort)
                msg = "Mã OTP đã hết hạn. Vui lòng yêu cầu mã mới."
            else:
                msg = "Mã OTP không tồn tại hoặc đã hết hạn. Vui lòng yêu cầu mã mới."

            logger.warning(f"OTP verification failed - no data found for: {email} (ttl={ttl})")
            raise HTTPException(status_code=400, detail=msg)

        attempts = int(data.get("attempts", 0))
        stored_otp = data.get("code", "")

        # Check if OTP matches
        if otp == stored_otp:
            # Success - set verified flag (do not delete OTP immediately to allow reset)
            ttl = await redis_service.get_otp_ttl(email)
            # Use remaining TTL if available, otherwise default
            remaining_ttl = ttl if ttl and ttl > 0 else OTP_TTL_SECONDS
            await redis_service.set_verified_flag(email, remaining_ttl)
            logger.info(f"OTP verified successfully for: {email}")
            return Message(status="success", message="Mã OTP đã được xác minh thành công")

        # Wrong OTP - increment attempts
        attempts += 1

        if attempts >= MAX_ATTEMPTS:
            # Maximum attempts reached - lock out
            await redis_service.delete_otp(email)
            logger.warning(f"Maximum OTP attempts reached for: {email}")
            raise HTTPException(
                status_code=400,
                detail="Đã vượt quá số lần thử tối đa. Vui lòng yêu cầu mã mới."
            )

        # Update attempts counter
        await redis_service.update_otp_attempts(email, attempts)
        logger.warning(f"Invalid OTP attempt {attempts}/{MAX_ATTEMPTS} for: {email}")

        remaining_attempts = MAX_ATTEMPTS - attempts
        raise HTTPException(
            status_code=400,
            detail=f"Mã OTP không đúng. Còn {remaining_attempts} lần thử nữa."
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in verify_password_reset_otp: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

async def reset_password_with_otp(email: str, otp: str, new_password: str, db: AsyncSession) -> Message:
    """
    Reset password using verified OTP
    
    Args:
        email: User email address
        otp: Verified OTP code  
        new_password: New password to set
        db: Database session
        
    Returns:
        Message: Response with status and message
        
    Raises:
        HTTPException: Various HTTP exceptions for different scenarios
    """
    try:
        # Validate inputs
        if not _validate_email_format(email):
            raise HTTPException(status_code=400, detail="Định dạng email không hợp lệ")

        if not otp or len(otp.strip()) != OTP_LENGTH:
            raise HTTPException(status_code=400, detail=f"Mã OTP phải gồm đúng {OTP_LENGTH} chữ số")

        # Validate password strength
        is_valid, password_message = _validate_password_strength(new_password)
        if not is_valid:
            raise HTTPException(status_code=400, detail=password_message)

        # Normalize inputs
        email = email.lower().strip()
        otp = otp.strip()

        # Verify OTP again (double-check security)
        data = await redis_service.get_otp(email)
        if not data:
            try:
                ttl = await redis_service.get_otp_ttl(email)
            except Exception:
                ttl = None

            if ttl == -2:
                msg = "Không tìm thấy mã OTP. Vui lòng yêu cầu mã mới."
            elif isinstance(ttl, int) and ttl <= 0:
                msg = "Mã OTP đã hết hạn. Vui lòng yêu cầu mã mới."
            else:
                msg = "Mã OTP không tồn tại hoặc đã hết hạn. Vui lòng yêu cầu mã mới."

            logger.warning(f"Password reset failed - no OTP data for: {email} (ttl={ttl})")
            raise HTTPException(status_code=400, detail=msg)

        attempts = int(data.get("attempts", 0))
        stored_otp = data.get("code", "")

        if otp != stored_otp:
            # Wrong OTP - increment attempts and possibly lock out
            attempts += 1
            if attempts >= MAX_ATTEMPTS:
                await redis_service.delete_otp(email)
                logger.warning(f"Password reset blocked - max attempts for: {email}")
                raise HTTPException(
                    status_code=400,
                    detail="Đã vượt quá số lần thử tối đa. Vui lòng yêu cầu mã mới."
                )

            await redis_service.update_otp_attempts(email, attempts)
            remaining_attempts = MAX_ATTEMPTS - attempts
            raise HTTPException(
                status_code=400,
                detail=f"Mã OTP không đúng. Còn {remaining_attempts} lần thử nữa."
            )

        # OTP is correct - proceed with password reset
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()

        if not user:
            # Clean up and return generic message for security
            await redis_service.delete_otp(email)
            logger.warning(f"Password reset attempted for non-existent user: {email}")
            return Message(status="success", message="Password reset processed")

        # Hash new password and update user
        hashed_password = hash_password(new_password)
        user.password = hashed_password

        # Update last password change timestamp if you have that field
        # user.password_changed_at = datetime.utcnow()

        await db.commit()

        # Clean up OTP
        await redis_service.delete_otp(email)

        # Send confirmation email (best effort - don't fail if this fails)
        try:
            await email_service.send_password_reset_success_email(email)
        except Exception as e:
            logger.error(f"Failed to send confirmation email to {email}: {str(e)}")

        logger.info(f"Password reset successful for: {email}")
        return Message(status="success", message="Password has been reset successfully")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in reset_password_with_otp: {str(e)}")
        try:
            await db.rollback()  # Rollback transaction on error
        except Exception:
            pass
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

# Health check function for monitoring
async def health_check() -> dict:
    """Check if forgot password service dependencies are healthy"""
    try:
        # Check Redis connection
        await redis_service._check_connection()
        
        # Check if email service is configured
        if not hasattr(email_service, 'smtp_server'):
            return {"status": "unhealthy", "reason": "Email service not configured"}
            
        return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}
        
    except Exception as e:
        return {"status": "unhealthy", "reason": str(e)}
