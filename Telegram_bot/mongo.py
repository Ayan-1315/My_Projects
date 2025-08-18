from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
from config import MONGO_DB_URI

db = None
modelist = {}

# Initialize MongoDB connection if URI is provided
if MONGO_DB_URI:
    mongo = MongoClient(MONGO_DB_URI)
    db = mongo.ChatBot
    users_db = db.users
    blocked_db = db.block
    mode_db = db.mode
else:
    users_db = blocked_db = mode_db = None  # Fallback to None if no URI

# Served Users
async def is_served_user(user_id: int) -> bool:
    if users_db:
        user = await users_db.find_one({"user_id": user_id})
        return bool(user)
    return False

async def get_served_users() -> list:
    if users_db:
        return [user async for user in users_db.find({"user_id": {"$gt": 0}})]
    return []

async def add_served_user(user_id: int):
    if users_db and not await is_served_user(user_id):
        await users_db.insert_one({"user_id": user_id})

# Banned Users
async def get_banned_users() -> list:
    if blocked_db:
        return [user["user_id"] async for user in blocked_db.find({"user_id": {"$gt": 0}})]
    return []

async def get_banned_count() -> int:
    if blocked_db:
        users = await blocked_db.find({"user_id": {"$gt": 0}}).to_list(length=100000)
        return len(users)
    return 0

async def is_banned_user(user_id: int) -> bool:
    if blocked_db:
        user = await blocked_db.find_one({"user_id": user_id})
        return bool(user)
    return False

async def add_banned_user(user_id: int):
    if blocked_db and not await is_banned_user(user_id):
        await blocked_db.insert_one({"user_id": user_id})

async def remove_banned_user(user_id: int):
    if blocked_db and await is_banned_user(user_id):
        await blocked_db.delete_one({"user_id": user_id})

# Forward Mode
async def is_group(chat_id: int) -> bool:
    if mode_db:
        if chat_id not in modelist:
            user = await mode_db.find_one({"chat_id": chat_id})
            modelist[chat_id] = bool(user)
        return modelist[chat_id]
    return False

async def group_on(chat_id: int):
    if mode_db:
        modelist[chat_id] = True
        if not await mode_db.find_one({"chat_id": chat_id}):
            await mode_db.insert_one({"chat_id": chat_id})

async def group_off(chat_id: int):
    if mode_db:
        modelist[chat_id] = False
        if await mode_db.find_one({"chat_id": chat_id}):
            await mode_db.delete_one({"chat_id": chat_id})
