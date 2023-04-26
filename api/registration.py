from fastapi import FastAPI,APIRouter
from pydantic import BaseModel
import sqlite3

router_registration = APIRouter()

class User(BaseModel):
    username: str
    password: str
    email: str

@router_registration.post("/register")
def register(user: User):
    conn = sqlite3.connect('users.dbo')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username text, password text, email text)''')
    c.execute("SELECT * FROM users WHERE username = ?", (user.username,))
    data = c.fetchone()
    if data:
        return {"message": "User already exists"}
    else:
        c.execute("INSERT INTO users VALUES (?, ?, ?)", (user.username, user.password, user.email))
        conn.commit()
        return {"message": "User registered successfully"}
    conn.close()
