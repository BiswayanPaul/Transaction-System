from pydantic import BaseModel
from beanie import PydanticObjectId


class AddCreditsModel(BaseModel):
    facility_id: PydanticObjectId
    user_id: PydanticObjectId
    amount: int


class DeductCreditsModel(BaseModel):
    facility_id: PydanticObjectId
    user_id: PydanticObjectId
    service_id: str
    tokens: int


class AddServiceModel(BaseModel):
    service_name: str
    credits_per_unit: int
    description: str


class AddLogCredit(BaseModel):
    facility_id: PydanticObjectId
    user_id: PydanticObjectId
    type: str
    amount: int


class AddLogService(BaseModel):
    service_id: PydanticObjectId
    service_name: str
    tokens: int
