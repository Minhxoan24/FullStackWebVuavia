from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

# Use the MessageSchema for consistent error/success payloads
from app.schemas.Message.Message import MessageSchema

# Import tất cả models TRƯỚC KHI tạo FastAPI app để đăng ký mappers


from app.endpoints.v1 import Account, Category ,Order  ,TypeProduct ,Voucher , AccountVuavia , TransactionHistory , InformationTypeProduct , Deposit

app = FastAPI(title="Vuavia API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://yourdomain.com"],  # Thay bằng domain thực tế
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(Account.router)
app.include_router(Category.router)
app.include_router(TypeProduct.router)
app.include_router(AccountVuavia.router)

app.include_router(Order.router)
app.include_router(Voucher.router)
app.include_router(TransactionHistory.router)
app.include_router(InformationTypeProduct.router)
app.include_router(Deposit.router)


# Global handler for HTTPException to return MessageSchema JSON
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    # exc.detail may be string or other; normalize to string message
    detail = exc.detail
    message = detail if isinstance(detail, str) else (detail.get('message') if isinstance(detail, dict) else str(detail))
    payload = MessageSchema(status="error", message=str(message)).dict()
    return JSONResponse(status_code=exc.status_code, content=payload)


# Generic exception handler to avoid exposing stack traces
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    # Log is handled elsewhere; return generic message
    payload = MessageSchema(status="error", message="Internal server error").dict()
    return JSONResponse(status_code=500, content=payload)


# .\venv\Scripts\Activate.ps1
# uvicorn app.main:app --reload
# uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 
# http://127.0.0.1:8000/docs