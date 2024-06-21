import motor.motor_asyncio
import os
from dotenv import load_dotenv
from bson.objectid import ObjectId

load_dotenv()  # Load environment variables from .env file

MONGO_DETAILS = os.getenv("MONGO_DETAILS")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.credit_system


balance_collection = database.get_collection("balances")
service_collection = database.get_collection("services")
log_collection_credits = database.get_collection("log_credits")
log_collection_services = database.get_collection("log_services")
