from pydantic import BaseModel

class InformationTypeProductBase(BaseModel):
    describe: dict
    type_product_id: int

class InformationTypeProductCreate(InformationTypeProductBase):
    pass

class InformationTypeProductUpdate(InformationTypeProductBase):
    pass

