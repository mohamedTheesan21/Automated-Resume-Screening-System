from fastapi import FastAPI, HTTPException, Depends, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
from Database import add_user, user_exists, db
from Models import UserModel, UserAuth
from motor.motor_asyncio import AsyncIOMotorGridFSBucket  # Use motor's GridFS

from datetime import timedelta, datetime, timezone
from typing import Optional, List

from dotenv import load_dotenv
import os
import pandas as pd
import io
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import numpy as np

from test2 import extract_entities

# JWT authentication
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt


app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
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
async def upload_pdfs(
    files: List[UploadFile] = File(...),
    skills: str = Form(...),
    education: str = Form(...),
    experience: str = Form(...),
):
    input_skills = skills.split(",")  # Convert the input string to a list of skills
    model = SentenceTransformer("paraphrase-MiniLM-L6-v2")
    input_education_embedding = model.encode(education)  # Create embedding for input education
    input_experience_embedding = model.encode(experience)  # Create embedding for input experience

    # Initialize an empty DataFrame to store all resume data
    all_resumes_df = pd.DataFrame(columns=['Name', 'Skills', 'Education', 'Experience', 'References', 'Score'])

    # Initialize a vectorizer for the provided skills
    vectorizer = CountVectorizer()
    skills_vector = vectorizer.fit_transform([skills])

    for file in files:
        if file.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")
        else:
            # Read the file as bytes
            file_content = await file.read()
        
            # Convert bytes to a BytesIO object to be compatible with pdfminer
            pdf_io = io.BytesIO(file_content)
            
            # Process the file and get the extracted entities as a DataFrame
            resume_df = extract_entities(pdf_io, file.filename, input_skills)
            
            # Append to the main DataFrame
            all_resumes_df = pd.concat([all_resumes_df, resume_df], ignore_index=True)

    # Calculate cosine similarity for each resume's skills, education, and experience
    for index, row in all_resumes_df.iterrows():
        resume_skills = row['Skills'].split(",")
        # Calculate skill similarity
        skill_similarity_score = calculate_skill_score(input_skills, resume_skills)
        
        # Calculate cosine similarity for education
        resume_education_embedding = model.encode(row['Education'])
        education_similarity_score = cosine_similarity(
            [input_education_embedding], [resume_education_embedding]
        )[0][0]

        # Calculate cosine similarity for experience
        resume_experience_embedding = model.encode(row['Experience'])
        experience_similarity_score = cosine_similarity(
            [input_experience_embedding], [resume_experience_embedding]
        )[0][0]

        # Calculate the final score with weighted average (60% Skills, 20% Education, 20% Experience)
        final_score = (
            (skill_similarity_score * 0.6) + 
            (education_similarity_score * 0.2) + 
            (experience_similarity_score * 0.2)
        )
        # print("index", index)
        # print("skill_similarity_score", skill_similarity_score)
        # print("education_similarity_score", education_similarity_score)
        # print("experience_similarity_score", experience_similarity_score)
        # print("/n")
        # Assign final score to the DataFrame row
        all_resumes_df.at[index, 'Score'] = final_score

    # Save the combined DataFrame to a CSV file
    all_resumes_df.to_csv("all_resumes_data.csv", index=False)
    
    return {"msg": "Files processed and saved to CSV successfully."}

def calculate_skill_score(input_skills, resume_skills):
    model = SentenceTransformer("paraphrase-MiniLM-L6-v2")
    
    # Embed each skill in both input_skills and resume_skills
    input_skills_embeddings = model.encode(input_skills)
    resume_skills_embeddings = model.encode(resume_skills)
    
    # Compute pairwise cosine similarity
    similarity_matrix = cosine_similarity(input_skills_embeddings, resume_skills_embeddings)
    
    # Calculate the maximum similarity for each input skill
    max_similarities = np.max(similarity_matrix, axis=1)
    
    # Calculate the average similarity score for skills
    skill_score = np.mean(max_similarities)
    
    return skill_score