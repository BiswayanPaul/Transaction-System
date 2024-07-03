from fastapi import APIRouter, HTTPException
from pymongo.errors import PyMongoError
from xempla.database.models.ai.credit_system.tranactions import BalanceCollection, ServiceCollection, LogCollectionService
from xempla.schemas.ai_credit_service import AddCreditsReponseModel, AddServiceRequestModel, AddServiceResponseModel
from beanie import PydanticObjectId
from datetime import datetime, timezone

class ServiceCore:
    @staticmethod
    async def add_service(service_name,credits_per_unit,description):
        try:
            service = await ServiceCollection.find_one({"service_name": service_name})
            if service:
                raise HTTPException(status_code=400, detail="Service already exists")
             
            new_service = ServiceCollection(service_name=service_name, credits_per_unit=credits_per_unit,description=description)
            await new_service.insert() 
            new_log = LogCollectionService(service_id=new_service.id,service_name=new_service.service_name,time_created=datetime.now(timezone.utc))
            await new_log.insert()
            
            response_log = AddServiceResponseModel(id=new_log.id,service_name=new_log.service_name)
            return response_log
        
        except Exception as e:
            raise HTTPException(status_code=500, detail="Problem outside" + str(e))
