import motor.motor_asyncio

MONGO_URL="mongodb://localhost:27017"


client=motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)

db=client.students_database

collection=db.students_collection


