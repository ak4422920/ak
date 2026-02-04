from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timedelta
from config import MONGO_URI, VERIFY_EXPIRE_HOURS

# MongoDB Connection
client = AsyncIOMotorClient(MONGO_URI)
db = client["multibot_db"]

# Collections
users_col = db["users"]
batches_col = db["batches"]

# --- [ USER LOGIC ] ---

async def get_user(user_id):
    """User ka data nikalna ya naya user create karna"""
    user = await users_col.find_one({"user_id": user_id})
    if not user:
        user = {
            "user_id": user_id,
            "points": 0,
            "is_verified": False,
            "last_verify": None,
            "referred_by": None,
            "joined_date": datetime.now()
        }
        await users_col.insert_one(user)
    return user

async def add_points(user_id, points):
    """Points badhane ke liye"""
    await users_col.update_one({"user_id": user_id}, {"$inc": {"points": points}})

# --- [ VERIFICATION LOGIC (20-Hour Rule) ] ---

async def is_user_verified(user_id):
    """Check karna ki kya 20 ghante wala link abhi valid hai"""
    user = await get_user(user_id)
    if not user.get("last_verify"):
        return False
    
    # Check if time has expired
    expiry_time = user["last_verify"] + timedelta(hours=VERIFY_EXPIRE_HOURS)
    if datetime.now() < expiry_time:
        return True
    return False

async def update_verify_status(user_id):
    """Shortlink complete hone par verification time reset karna"""
    await users_col.update_one(
        {"user_id": user_id}, 
        {"$set": {"last_verify": datetime.now(), "is_verified": True}}
    )

# --- [ BATCH LOGIC ] ---

async def save_batch(batch_id, file_ids):
    """Random batch ko database mein save karna taaki user link pe click kare toh use files milein"""
    await batches_col.insert_one({
        "batch_id": batch_id,
        "files": file_ids,
        "created_at": datetime.now()
    })

async def get_batch(batch_id):
    """Batch ID se files nikalna"""
    return await batches_col.find_one({"batch_id": batch_id})
