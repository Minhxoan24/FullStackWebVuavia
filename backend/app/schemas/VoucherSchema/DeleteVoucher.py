from pydantic import BaseModel


class DeleteVoucher(BaseModel):
    voucher_id: int 