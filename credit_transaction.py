from fastapi import APIRouter, Depends, status, Query
from typing import Any, List

from xempla.schemas import (
    AddCreditsRequestModel, AddCreditsReponseModel,UseCreditsRequestModel,AddServiceResponseModel,AddServiceRequestModel,FetchCreditRequestModel
)
from xempla.utils.json_serializer import make_serializable
from xempla.api.v1.deps import get_current_active_user
from xempla.database.models.user import ApiUser
from xempla.utils.cbv import as_view
from xempla.utils.types import PyObjectId
from beanie import PydanticObjectId
from xempla.core.ai.credit_system.credit_crud import (
    TransactionCore
)
from xempla.core.ai.credit_system.service_crud import (
    ServiceCore
)

router = APIRouter(
    responses={
        401: {
            "description": "Unauthorized, invalid credentials or access token",
        },
    },
)


@as_view(router)
class CreditSystemViews:
    user: ApiUser = Depends(get_current_active_user)

    @router.post("/add-credit", response_model= AddCreditsReponseModel, status_code=status.HTTP_201_CREATED)
    async def add_credit(self,credit_data : AddCreditsRequestModel):
        return await TransactionCore.add_credits(
            facility_id=credit_data.Facility_id,
            user_id=credit_data.User_id,
            amount = credit_data.amount
        )
    
    @router.post("/add-service", response_model=AddServiceResponseModel , status_code=status.HTTP_201_CREATED)
    async def add_services(self,credit_data : AddServiceRequestModel):
        return await ServiceCore.add_service(
            service_name=credit_data.service_name,
            credits_per_unit=credit_data.credits_per_unit,
            description=credit_data.description
        )
    
    @router.post("/use-credit", response_model= AddCreditsReponseModel,status_code=status.HTTP_201_CREATED)
    async def use_credit(self,credit_data : UseCreditsRequestModel):
        return await TransactionCore.use_credits(
            facility_id=credit_data.facility_id,
            user_id=credit_data.user_id,
            service_name = credit_data.service_name,
            tokens = credit_data.tokens
        )
    
    @router.get("/fetch-credits/{facility_id}",status_code=status.HTTP_201_CREATED)
    async def fetch_credit(self,facility_id:PydanticObjectId):
        return await TransactionCore.fetch_credits(
            facility_id=facility_id,
        )

