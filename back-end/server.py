from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from Database import add_user, user_exists
from Models import UserModel

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (POST, GET, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Simulated database
fake_users_db = {}

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

@app.post("/signup")
async def signup(user: UserModel):
    existing_user = await user_exists(user.email) 
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash the user's password
    hashed_password = hash_password(user.password)
    user.password = hashed_password

    user_data = user.model_dump()
    new_user = await add_user(user_data)
    return {"msg": "User created successfully"}

@app.post("/login")
async def login(email: EmailStr, password: str):
    user = await user_exists(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verify the password
    if not verify_password(password, user["password"]):
        raise HTTPException(status_code=400, detail="Invalid password")
    
    return {"msg": "Login successful"}
    
    

