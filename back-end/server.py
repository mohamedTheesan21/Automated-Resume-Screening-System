from fastapi import FastAPI, HTTPException, Depends, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
from Database import add_user, user_exists, db
from Models import UserModel, UserAuth
from motor.motor_asyncio import AsyncIOMotorGridFSBucket  # Use motor's GridFS

from datetime import timedelta, datetime, timezone
from typing import Optional, List

from dotenv import load_dotenv
import os

# JWT authentication
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt


app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (POST, GET, etc.)
    allow_headers=["*"],  # Allows all headers
)

bucket = AsyncIOMotorGridFSBucket(db)

# Load environment variables from .env file
load_dotenv()

secret_key = os.getenv("SECRET_KEY")
algorithm = os.getenv("ALGORITHM")
token_expiration = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# JWT Token Creation
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt

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
async def login(user: UserAuth):
    existing_user = await user_exists(user.email)
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verify the password
    if not verify_password(user.password, existing_user["password"]):
        raise HTTPException(status_code=400, detail="Invalid password")
    
    token_expiration_minutes = int(token_expiration)
    
    # create jwt token
    access_token_expires = timedelta(minutes=token_expiration_minutes)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


# Dependency to get current user
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await user_exists(email)
    if user is None:
        raise credentials_exception
    return user

@app.get("/protected")
async def protected_route(current_user: UserModel = Depends(get_current_user)):
    return {"user": current_user}

@app.post("/upload")
async def upload_pdfs(files: List[UploadFile] = File(...) ):
    file_ids = []
    for file in files:
        if file.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")
        else:
            # Read the file data
            file_data = await file.read()

            # Save the file to GridFS using motor's GridFSBucket
            try:
                grid_in = bucket.open_upload_stream(
                    file.filename,
                    metadata={"content_type": file.content_type}
                )
                await grid_in.write(file_data)
                await grid_in.close()

                # Append file ID to the list
                file_ids.append(str(grid_in._id))
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"An error occurred while uploading the file: {str(e)}")

            # Append the file ID (from GridFS) to the list
            file_ids.append(str(grid_in._id))
    
    return {"file_ids": file_ids, "msg": "Files uploaded successfully"}