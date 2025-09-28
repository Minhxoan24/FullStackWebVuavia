from fastapi import HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Tuple, Optional
import cloudinary
import cloudinary.uploader as uploader
from sqlalchemy import select
import io

# non-blocking helpers
import asyncio
from concurrent.futures import ThreadPoolExecutor

from app.service.AccountService.UpdateAvtService import update_user_avatar
from app.models.Users import User
from app.core.config import CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET

# Config Cloudinary
cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET
)

ALLOWED_MIMES = {"image/jpeg", "image/png", "image/webp"}
MAX_SIZE_MB = 5
MAX_SIZE_BYTES = MAX_SIZE_MB * 1024 * 1024

def _validate_file_meta(file: UploadFile):
    if file.content_type not in ALLOWED_MIMES:
        raise HTTPException(status_code=400, detail="Chỉ chấp nhận JPG/PNG/WebP")

async def _read_with_limit(file: UploadFile) -> bytes:
    content = await file.read()
    if len(content) > MAX_SIZE_BYTES:
        raise HTTPException(status_code=400, detail=f"Kích thước ảnh vượt {MAX_SIZE_MB}MB")
    return content

# executor cho upload/destroy blocking
_executor = ThreadPoolExecutor(max_workers=3)

async def _upload_to_cloudinary(content: bytes) -> Tuple[str, Optional[str]]:
    """
    Upload non-blocking trong threadpool.
    Trả về (secure_url, public_id).
    """
    loop = asyncio.get_event_loop()

    def _upload():
        try:
            return uploader.upload(
                io.BytesIO(content),
                cloud_name=CLOUDINARY_CLOUD_NAME,
                api_key=CLOUDINARY_API_KEY,
                api_secret=CLOUDINARY_API_SECRET,
                folder="app/avatars",
                overwrite=False,
                unique_filename=True,
                resource_type="image",
                transformation=[{"width": 512, "height": 512, "crop": "fill", "gravity": "face"}],
            )
        except Exception as e:
            raise RuntimeError(f"Cloudinary upload failed: {e}")

    try:
        res = await loop.run_in_executor(_executor, _upload)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload thất bại: {e}")

    new_url = res.get("secure_url") or res.get("url")
    new_public_id = res.get("public_id")
    if not new_url:
        raise HTTPException(status_code=500, detail="Không nhận được secure_url từ Cloudinary")
    return new_url, new_public_id

async def _destroy_cloudinary(public_id: str) -> None:
    """
    Xóa ảnh cũ trên Cloudinary (best-effort). Chạy trong executor.
    """
    if not public_id:
        return
    loop = asyncio.get_event_loop()

    def _destroy():
        try:
            uploader.destroy(public_id, invalidate=True, resource_type="image")
        except Exception:
            # best-effort: không raise lỗi cho user nếu xóa fail
            pass

    await loop.run_in_executor(_executor, _destroy)

async def update_user_avatar_service(
    db: AsyncSession,
    user_id: int,
    file: UploadFile
) -> str:
    """
    Validate -> upload -> update DB.
    Lưu cả avatar (url) và avatar_public_id (nếu có).
    Nếu user đã có avatar_public_id trước đó, thực hiện xóa cũ (best-effort) trong background.
    Trả về URL mới.
    """
    try:
        _validate_file_meta(file)
        content = await _read_with_limit(file)

        # load user
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="Người dùng không tồn tại")

        old_public_id = getattr(user, "avatar_public_id", None)

        # upload (non-blocking)
        new_url, new_public_id = await _upload_to_cloudinary(content)

        # update DB: gọi service cập nhật, service nên chấp nhận avatar_public_id (nullable)
        await update_user_avatar(db, user_id, new_url, new_public_id)

        # xóa ảnh cũ trong background (best-effort) — không chặn response
        if old_public_id and new_public_id and old_public_id != new_public_id:
            # schedule background task
            try:
                asyncio.create_task(_destroy_cloudinary(old_public_id))
            except Exception:
                # nếu không thể tạo task thì bỏ qua — không ảnh hưởng tới response
                pass

        return new_url

    except HTTPException:
        raise
    except Exception as e:
        try:
            await db.rollback()
        except Exception:
            pass
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

