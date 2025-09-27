import redis.asyncio as redis
import json
from fastapi import HTTPException
from typing import Optional, Dict, Any
import asyncio
from datetime import datetime, timedelta

class RedisService:
    def __init__(self, host: str = "localhost", port: int = 6379, decode_responses: bool = True):
        self.client = redis.Redis(host=host, port=port, decode_responses=decode_responses)
        self._connection_checked = False

    async def _check_connection(self):
        """Kiểm tra kết nối Redis"""
        if not self._connection_checked:
            try:
                await self.client.ping()
                self._connection_checked = True
            except Exception as e:
                raise HTTPException(
                    status_code=503, 
                    detail=f"Redis connection failed: {str(e)}. Please ensure Redis server is running."
                )

    async def set_voucher_cache(self, user_id: int, voucher_data: Dict[str, Any], ttl: int = 1800) -> None:
        """Lưu thông tin voucher tạm vào Redis với TTL (mặc định 30 phút)."""
        await self._check_connection()
        cache_key = f"voucher_temp:{user_id}"
        try:
            await self.client.setex(cache_key, ttl, json.dumps(voucher_data))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to set voucher cache: {str(e)}")

    async def get_voucher_cache(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Lấy thông tin voucher từ Redis."""
        await self._check_connection()
        cache_key = f"voucher_temp:{user_id}"
        try:
            cached_data = await self.client.get(cache_key)
            return json.loads(cached_data) if cached_data else None
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get voucher cache: {str(e)}")

    async def delete_voucher_cache(self, user_id: int) -> None:
        """Xóa voucher tạm khỏi Redis."""
        await self._check_connection()
        cache_key = f"voucher_temp:{user_id}"
        try:
            await self.client.delete(cache_key)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to delete voucher cache: {str(e)}")

    # ==== Forgot Password OTP helpers ====
    def _daily_counter_key(self, email: str) -> str:
        today = datetime.utcnow().strftime('%Y-%m-%d')
        return f"otp:send_count:{email}:{today}"

    def _otp_key(self, email: str) -> str:
        return f"otp:code:{email}"

    def _seconds_until_midnight_utc(self) -> int:
        now = datetime.utcnow()
        tomorrow = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        return int((tomorrow - now).total_seconds())

    async def get_daily_send_count(self, email: str) -> int:
        await self._check_connection()
        key = self._daily_counter_key(email)
        value = await self.client.get(key)
        return int(value) if value is not None else 0

    async def increment_daily_send(self, email: str) -> int:
        """Tăng bộ đếm gửi OTP theo ngày và set TTL tới 0h UTC ngày hôm sau nếu mới tạo."""
        await self._check_connection()
        key = self._daily_counter_key(email)
        count = await self.client.incr(key)
        # Nếu mới tạo (trước đó chưa có TTL), đặt TTL tới nửa đêm
        ttl = await self.client.ttl(key)
        if ttl == -1:
            await self.client.expire(key, self._seconds_until_midnight_utc())
        return count

    async def set_otp(self, email: str, code: str, ttl_seconds: int = 180) -> None:
        await self._check_connection()
        key = self._otp_key(email)
        data = {"code": code, "attempts": 0}
        await self.client.setex(key, ttl_seconds, json.dumps(data))

    async def get_otp(self, email: str) -> Optional[Dict[str, Any]]:
        await self._check_connection()
        key = self._otp_key(email)
        raw = await self.client.get(key)
        return json.loads(raw) if raw else None

    async def update_otp_attempts(self, email: str, attempts: int) -> None:
        await self._check_connection()
        key = self._otp_key(email)
        raw = await self.client.get(key)
        if not raw:
            return
        obj = json.loads(raw)
        obj["attempts"] = attempts
        # giữ nguyên TTL còn lại
        ttl = await self.client.ttl(key)
        if ttl and ttl > 0:
            await self.client.setex(key, ttl, json.dumps(obj))
        else:
            await self.client.delete(key)

    async def delete_otp(self, email: str) -> None:
        await self._check_connection()
        await self.client.delete(self._otp_key(email))

    async def close(self):
        """Đóng kết nối Redis"""
        await self.client.close()

    # ==== New helpers for OTP verification flow ====
    async def get_otp_ttl(self, email: str) -> int:
        """Return remaining TTL for the OTP key in seconds. Returns -2 if key does not exist, -1 if no TTL."""
        await self._check_connection()
        key = self._otp_key(email)
        ttl = await self.client.ttl(key)
        return int(ttl) if ttl is not None else -2

    async def set_verified_flag(self, email: str, ttl_seconds: int) -> None:
        """Set a short-lived verified flag for the email so reset endpoint can proceed."""
        await self._check_connection()
        key = f"otp:verified:{email}"
        # Use same TTL as remaining OTP or provided ttl_seconds
        ttl = int(ttl_seconds) if ttl_seconds and int(ttl_seconds) > 0 else 180
        await self.client.setex(key, ttl, "1")

    async def is_verified(self, email: str) -> bool:
        """Check if the email has a verified flag in Redis."""
        await self._check_connection()
        key = f"otp:verified:{email}"
        val = await self.client.get(key)
        return val is not None

    async def delete_verified_flag(self, email: str) -> None:
        """Delete verified flag for an email."""
        await self._check_connection()
        await self.client.delete(f"otp:verified:{email}")

# Khởi tạo RedisService
redis_service = RedisService()