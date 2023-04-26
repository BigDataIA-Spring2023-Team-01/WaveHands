from fastapi import HTTPException
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
import sqlite3
from datetime import datetime
import api.jwt as jwt

router_user = APIRouter()


class User(BaseModel):
    username: str
    password: str  
    plan: str


class User_Details(BaseModel):
    hashed_password: str | None = None
    register_time: str | None = None
    role: str | None = 'user'
    email:str | None = None
    status:str | None = 'active'

class Change_Password(BaseModel):
    username: str
    password: str  
    confirm_password: str


@router_user.post("/register")
async def register_user(user: User):
    
    User_Details.hashed_password = jwt.get_password_hash(user.password)
    User_Details.register_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    User_Details.role = "user"
    User_Details.email = "{}@gmail.com".format(user.username)
    User_Details.status = "active"
# Define the table schema
    conn = sqlite3.connect('data/users.db')
    c = conn.cursor()

    try:
        query = "INSERT INTO USER_DATA (username, email, password, status, role, plan, register_time) VALUES (?, ?, ?, ?, ?, ?, ?)"
        c.execute(query, (user.username,User_Details.email,User_Details.hashed_password,User_Details.status,User_Details.role,user.plan,User_Details.register_time))
        conn.commit()
        conn.close()
        return {"Success"}
    except:
        raise HTTPException(status_code=400, detail="user already exists")
           
    

    


@router_user.put("/update_password")
async def update_password(data: Change_Password):
   
    # Update the user's password in the dictionary
    # if username in users['username']:
    username = data.username
    password = data.password
    confirm_password = data.confirm_password
    if password != confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    elif password != " ":
        password = jwt.get_password_hash(password)
        conn = sqlite3.connect('data/users.db')
        c = conn.cursor()
        query = "UPDATE USER_DATA SET password = ? WHERE username = ?"
        c.execute(query, (password, username))
        conn.commit()
        conn.close()
        return {"successfully changed password"}

    else:
        raise HTTPException(status_code=500, detail="User not found")






