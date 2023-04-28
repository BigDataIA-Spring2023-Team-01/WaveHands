from fastapi import FastAPI,Request
import os
from dotenv import load_dotenv
from api import signconversion,jwt,registration,wordbook
load_dotenv()

secret_key = os.environ.get("SECRET_KEY")
app = FastAPI()


app.include_router(signconversion.router_signconversion)
app.include_router(jwt.router_jwt)
app.include_router(registration.router_user)
app.include_router(wordbook.router_wordbook)

@app.get("/test")
async def root(current_user: jwt.User = jwt.Depends(jwt.get_current_active_user)):
    return {"message": "Hello Bigger Applications!"}