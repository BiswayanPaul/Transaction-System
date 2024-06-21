from fastapi import APIRouter, HTTPException
from database import service_collection, log_collection_services
import datetime

router = APIRouter()


@router.post("/add-service")
async def add_service(service_name: str, credits_per_unit: int, description: str):
    service = await service_collection.find_one({"service_name": service_name})
    if service:
        raise HTTPException(status_code=400, detail="Service already exists")

    new_service = {
        "service_name": service_name, "credits_per_unit": credits_per_unit, "description": description}
    await service_collection.insert_one(new_service)
    print("reached")
    await log_collection_services.insert_one({"service_id": new_service["_id"], "service_name": new_service["service_name"], "time_created": datetime.datetime.now()})
    new_log = await log_collection_services.find().to_list(None)
    return_string = str(new_log[len(new_log)-1]["_id"])
    return return_string
