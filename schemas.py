from pydantic import BaseModel
import datetime
from beanie import PydanticObjectId


class UserBalanceSchema(BaseModel):
    facility_id: PydanticObjectId
    user_id: PydanticObjectId
    balance: int


class ServiceSchema(BaseModel):
    service_id: PydanticObjectId
    service_name: str
    credits_per_unit: int
    description: str


class LogCredit(BaseModel):
    facility_id: PydanticObjectId
    user_id: PydanticObjectId
    type: str
    amount: int
    time_created: datetime.datetime


class LogService(BaseModel):
    service_id: PydanticObjectId
    service_name: str
    time_created: datetime.datetime
