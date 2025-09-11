import redis.asyncio as redis
import json
from fastapi import HTTPException
from typing import Optional, Dict, Any
import asyncio

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

    async def close(self):
        """Đóng kết nối Redis"""
        await self.client.close()

# Khởi tạo RedisService
redis_service = RedisService()