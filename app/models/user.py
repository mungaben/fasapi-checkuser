# app/models/user.py
from pydantic import BaseModel, EmailStr,constr

class UserLogin(BaseModel):
    username: str
    password: str

class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: str
    username: str
    email: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut

class UserData(BaseModel):
    first_name: constr(min_length=1)
    last_name: constr(min_length=1)
    ssn: constr(min_length=9, max_length=9)
    city: constr(min_length=1)


class UserInput(BaseModel):
    first_name: str
    last_name: str
    dob: str
    ssn: str
    city: str