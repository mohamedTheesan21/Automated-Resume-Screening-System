from motor.motor_asyncio import AsyncIOMotorClient

# Create a client instance
conn = AsyncIOMotorClient("mongodb+srv://admin:12345@myatlasclusteredu.zdyf7zp.mongodb.net/ARSS_DB")
db = conn.ARSS_DB

def user_helper(user) -> dict:
    return {
        "name": user["name"],
        "email": user["email"],
        "password": user["password"],
    }

# Retrieve all users
async def retrieve_users():
    users = []
    # Dynamically get the collection
    collection_name = db["users"]  # 'users' collection will be created on first insert
    async for user in collection_name.find():
        users.append(user_helper(user))
    return users

# Add a new user
async def add_user(user_data):
    collection_name = db["users"]  # 'users' collection will be created on first insert
    user = await collection_name.insert_one(user_data)
    new_user = await collection_name.find_one({"_id": user.inserted_id})
    return user_helper(new_user)

# check if user exists
async def user_exists(email: str):
    collection_name = db["users"]
    user = await collection_name.find_one({"email": email})
    return user