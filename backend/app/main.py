from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import tất cả models TRƯỚC KHI tạo FastAPI app để đăng ký mappers
from app.models import *

from app.endpoints.v1 import Account, Category ,Order  ,TypeProduct ,Voucher , AccountVuavia , TransactionHistory , InformationTypeProduct

app = FastAPI(title="Vuavia API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Trong production nên chỉ định cụ thể domain
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
# .\venv\Scripts\activate
# uvicorn app.main:app --reload
# uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 
# http://127.0.0.1:8000/docs