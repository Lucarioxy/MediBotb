from enum import Enum
from pydantic import BaseModel, Field, validator
from fastapi import UploadFile
from typing import Optional, List
from datetime import datetime

class Gender(str, Enum):
    male = "male"
    female = "female"
    non_binary = "non-binary"
    undisclosed = "undisclosed"

class ChatEntry(BaseModel):
    query: str
    response: str

class ChatDocument(BaseModel):
    user_id: str
    chats: List[ChatEntry] = []

class LoginUser(BaseModel):
    email: str
    password: str

class User(BaseModel):
    name: str
    email: str
    age: int
    height: int
    weight: int
    gender: Gender = Gender.undisclosed  # Default as 'undisclosed'
    password: str
    context: List[str] = [""]

    @validator('age')
    def validate_age(cls, value):
        if value < 0:
            raise ValueError('Age must be a positive number')
        return value
    
class Udisplay(BaseModel):
    user_id: str = Field(default_factory=str)
    name: str
    email: str
    age: int
    height: int
    weight: int
    gender: Gender = Gender.undisclosed  # Default as 'undisclosed'
    context: List[str] = [""]

    @validator('age')
    def validate_age(cls, value):
        if value < 0:
            raise ValueError('Age must be a positive number')
        return value

class Session(BaseModel):
    session_id: str = Field(default_factory=str)
    user_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_accessed: datetime = Field(default_factory=datetime.utcnow)
    context: str

class File(BaseModel):
    file_id: str = Field(default_factory=str)
    user_id: str
    filename: str
    upload_date: datetime = Field(default_factory=datetime.utcnow)
    file_type: str
    processed_text: Optional[str] = None

class FileUpload(BaseModel):
    user_id: str
    file: UploadFile
    
class ContextUpload(BaseModel):
    user_id: str
    context: str  
