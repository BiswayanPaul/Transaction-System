from fastapi import APIRouter, HTTPException
from pymongo.errors import PyMongoError
from xempla.database.models.ai.credit_system.tranactions import BalanceCollection, ServiceCollection, LogCollectionCredits
from xempla.schemas.ai_credit_service import AddCreditsReponseModel
from beanie import PydanticObjectId
from datetime import datetime, timezone



class TransactionCore:

    @staticmethod
    async def add_credits(facility_id:PydanticObjectId,user_id:PydanticObjectId,amount:int):
        try:
            # Attempt to find existing balance document
            print("Reached")
            balance = await BalanceCollection.find_one(BalanceCollection.facility_id == facility_id , BalanceCollection.user_id == user_id)
            print("reached")
            if balance:
                # Update existing balance
                previous_balance = balance.balance
                new_balance = balance.balance + amount
                balance.balance = balance.balance + amount
                await balance.save()
                transaction_type = "add"
            else:
                # Create new balance document
                previous_balance = int(0)
                new_balance = amount
                balance = BalanceCollection(facility_id=facility_id, user_id=user_id, balance=amount)
                await balance.insert()
                transaction_type = "create"

            # Log the transaction
            new_log = LogCollectionCredits(facility_id=facility_id,user_id=user_id,type=transaction_type,current_balance=new_balance,previous_balance=previous_balance,time_created=datetime.now(timezone.utc))
            await new_log.insert()
            response_log = AddCreditsReponseModel(id= new_log.id, previous_amt=previous_balance, current_amt=new_balance)
            return response_log
            # Return the _id of the newly inserted log entry
        except Exception as e:
            raise HTTPException(status_code=500, detail="Problem outside" + str(e))
        


    @staticmethod
    async def use_credits(facility_id:PydanticObjectId,user_id:PydanticObjectId,service_name:str, tokens):
        try:
            service = await ServiceCollection.find_one(ServiceCollection.service_name == service_name)
            if not service:
                raise HTTPException(
                    status_code=404, detail="Service not found")

            amount_to_deduct = tokens * service.credits_per_unit
            balance = await BalanceCollection.find_one(BalanceCollection.facility_id == facility_id , BalanceCollection.user_id == user_id)
            if not balance or balance.balance < amount_to_deduct:
                raise HTTPException(
                    status_code=400, detail="Insufficient balance")

            previous_balance = balance.balance
            new_balance = balance.balance - amount_to_deduct
            balance.balance = balance.balance - amount_to_deduct
            await balance.save()
            transaction_type = "deduct"

            new_log = LogCollectionCredits(facility_id=facility_id,user_id=user_id,type=transaction_type,current_balance=new_balance,previous_balance=previous_balance,time_created=datetime.now(timezone.utc))
            await new_log.insert()
            response_log = AddCreditsReponseModel(id= new_log.id, previous_amt=previous_balance, current_amt=new_balance)
            return response_log

        except PyMongoError as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    @staticmethod
    async def fetch_credits(facility_id):
        try:
            users = await LogCollectionCredits.find_many(LogCollectionCredits.facility_id == facility_id).to_list(length=None)
            if not users:
                raise HTTPException(
                status_code=404, detail="No users found for this facility")

            return users
        except PyMongoError as e:
            raise HTTPException(status_code=500, detail=str(e))