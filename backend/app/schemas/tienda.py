from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

#-----------Category Schemas-----------#
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):   
    id: int

    class Config:
        orm_mode = True     

#-----------Product Schemas-----------#
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: int
    stock: int
    category_id: int    

class ProductCreate(ProductBase):
    pass        

class Product(ProductBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True 

#-----------User Schemas-----------#
class UserBase(BaseModel):  
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    is_active: Optional[int] = 1    

class UserCreate(UserBase):
    password: str

class User(UserBase):   
    id: int

    class Config:
        orm_mode = True 


    