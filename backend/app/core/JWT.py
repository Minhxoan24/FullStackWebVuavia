from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES
from datetime import datetime, timedelta, timezone  # timedelta: khoảng thời gian, timezone: múi giờ
from typing import Optional
from jose import jwt, JWTError, ExpiredSignatureError
from fastapi import HTTPException
def create_access_token( data: dict ,time_token: Optional[timedelta] = None) -> str:
    data_use_encode = data.copy() 
    expire = datetime.now(timezone.utc) + ( time_token or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) ) # giờ utc + số phút hết hạn muốn cộng time thì sd time delta 
    data_use_encode.update ({"iat": datetime.now(timezone.utc), # cập nhật thời gian tạo token vào data payload 
                            "exp": expire ,  # cập nhật thời gian hết hạn vào data
                            "type_token": "access"} )# thêm type token vào data

    return jwt.encode(data_use_encode, SECRET_KEY, algorithm=ALGORITHM) # mã hóa dữ liệu thành token bằng secret key và thuật toán đã định nghĩa trong config
    # cú pháp tổng quát ( payload , secret_key , algorithm ) JWT = Header + Payload + Signature
def create_refresh_token(data : dict , time_token: Optional[timedelta] = None) -> str:
    data_use_encode = data.copy()
    expire = datetime.now(timezone.utc) + (time_token or timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES))  # giờ utc + số phút hết hạn muốn cộng time thì sd time delta
    data_use_encode.update({"iat": datetime.now(timezone.utc),  # cập nhật thời gian tạo token vào data payload
                           "exp": expire,  # cập nhật thời gian hết hạn vào data
                           "type_token": "refresh"}  # thêm type token vào data
    ) 
    return jwt.encode( data_use_encode , SECRET_KEY , algorithm=ALGORITHM) # mã hóa dữ liệu thành token bằng secret key và thuật toán đã định nghĩa trong config

def verify_access_token(token: str) -> dict:
    try:
        payload_decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  # giải mã token bằng secret key và thuật toán đã định nghĩa trong config
        if payload_decoded.get("type_token") not in ["access"]:              
            raise JWTError("Invalid token type")
        return payload_decoded  # trả về dữ liệu đã giải mã từ token
    except ExpiredSignatureError:  
        raise HTTPException(status_code=401, detail="Token has expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")  # nếu có lỗi trong quá trình giải mã, ném ra lỗi với status code 401 và thông báo "Invalid token"
def verify_refresh_token(token: str) -> dict:
    try:
        payload_decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  # giải mã token bằng secret key và thuật toán đã định nghĩa trong config
        if payload_decoded.get("type_token") not in ["refresh"]:              
            raise JWTError("Invalid token type")
        return payload_decoded  # trả về dữ liệu đã giải mã từ token
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")  # nếu có lỗi trong quá trình giải mã, ném ra lỗi với status code 401 và thông báo "Invalid token"
    
def create_full_token(data: dict, time_token: Optional[timedelta] = None) -> str:
    """Tạo token đầy đủ bao gồm access và refresh"""
    access_token = create_access_token(data, time_token)
    refresh_token = create_refresh_token(data, time_token)
    return{ 
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token type": "Bearer"  # Thêm type token để client biết cách sử dụng
    }