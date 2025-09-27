from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CreateDepositRequest(BaseModel):
    amount: float  # Số tiền user nhập