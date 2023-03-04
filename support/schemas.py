from pydantic import BaseModel

from typing import List


class FAQBase(BaseModel):
    title: str | None = None
    text: str | None 

class FAQUpdate(FAQBase):
    pass

    class Config:
        orm_mode = True
        
class FAQCreate(FAQBase):
    parent_id: None | int  = None

    class Config:
        orm_mode = True

class FAQBot(FAQBase):
    id: int | None 
    parent_id: int | None = None 
    
    class Config:
        orm_mode = True

class FAQ(FAQBase):
    id: int | None 
    parent_id: int | None = None 
    children: List["FAQ"]
    
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    is_active: bool | None = None

class Users(User):
    pass

    class Config:
        orm_mode = True

class UserInDB(User):
    hashed_password: str
    
    class Config:
        orm_mode = True