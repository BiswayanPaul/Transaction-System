from fastapi import APIRouter, HTTPException
from pymongo.errors import PyMongoError
from database import balance_collection, service_collection, log_collection_credits
from beanie import PydanticObjectId
import datetime

router = APIRouter()


@router.post("/add-credits")
async def add_credits(facility_id: PydanticObjectId, user_id: PydanticObjectId, amount: int):
    session = await balance_collection.database.client.start_session()
    async with session.start_transaction():
        try:
            balance = await balance_collection.find_one({"facility_id": facility_id, "user_id": user_id}, session=session)
            if balance:
                new_balance = balance["balance"] + amount
                await balance_collection.update_one({"_id": balance["_id"]}, {"$set": {"balance": new_balance}}, session=session)
                await log_collection_credits.insert_one({"facility_id": facility_id, "user_id": user_id, "type": "add", "balance": new_balance, "timestamp": datetime.datetime.now()}, session=session)
            else:
                new_balance = amount
                await balance_collection.insert_one({"facility_id": facility_id, "user_id": user_id, "balance": new_balance}, session=session)
                await log_collection_credits.insert_one({"facility_id": facility_id, "user_id": user_id, "type": "create", "balance": new_balance, "timestamp": datetime.datetime.now()}, session=session)
            await session.commit_transaction()
            new_log = await log_collection_credits.find().to_list(length=None)
            return_string = str(new_log[len(new_log)-1]["_id"])
            return return_string

        except PyMongoError as e:
            await session.abort_transaction()
            raise HTTPException(status_code=500, detail=str(e))


@router.post("/deduct-credits")
async def deduct_credits(facility_id: PydanticObjectId, user_id: PydanticObjectId, service_id: PydanticObjectId, tokens: int):
    session = await balance_collection.database.client.start_session()
    async with session.start_transaction():
        try:
            service = await service_collection.find_one({"_id": service_id}, session=session)
            if not service:
                raise HTTPException(
                    status_code=404, detail="Service not found")

            amount_to_deduct = tokens * service["credits_per_unit"]
            balance = await balance_collection.find_one({"facility_id": facility_id, "user_id": user_id}, session=session)
            if not balance or balance["balance"] < amount_to_deduct:
                raise HTTPException(
                    status_code=400, detail="Insufficient balance")

            new_balance = balance["balance"] - amount_to_deduct
            await balance_collection.update_one({"_id": balance["_id"]}, {"$set": {"balance": new_balance}}, session=session)
            await log_collection_credits.insert_one({"facility_id": facility_id, "user_id": user_id, "type": "deduct", "balance": new_balance, "timestamp": datetime.datetime.now()}, session=session)
            await session.commit_transaction()
            new_log = await log_collection_credits.find().to_list(length=None)
            return_string = str(new_log[len(new_log)-1]["_id"])
            return return_string

        except PyMongoError as e:
            await session.abort_transaction()
            raise HTTPException(status_code=500, detail=str(e))


@router.get("/fetch-credits")
async def fetch_credits(facility_id: PydanticObjectId):
    try:
        users = await log_collection_credits.find().to_list(length=None)
        if not users:
            raise HTTPException(
                status_code=404, detail="No users found for this facility")
        # print(users)
        user = []
        for i in users:
            if i["facility_id"] == facility_id:
                user.append(i)
        return_user = str(user)
        return return_user

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
