from pydantic import BaseModel, Field
from typing import Optional

class UserModel(BaseModel):
    name: str
    email: str
    password: str