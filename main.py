from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = FastAPI(
    title=os.getenv("APP_NAME", "Backend API"),
    version=os.getenv("APP_VERSION", "1.0")
)

# Temporary database
users = []

class User(BaseModel):
    id: int
    name: str
    email: str


@app.get("/")
def home():
    return {
        "message": "Welcome to FastAPI",
        "app": os.getenv("APP_NAME"),
        "environment": os.getenv("ENVIRONMENT")
    }


@app.get("/health")
def health():
    return {"status": "Running"}


@app.get("/users")
def get_users():
    return users


@app.post("/users")
def create_user(user: User):
    users.append(user)
    return {
        "message": "User Created",
        "user": user
    }


@app.get("/users/{user_id}")
def get_user(user_id: int):
    for user in users:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")


@app.put("/users/{user_id}")
def update_user(user_id: int, updated_user: User):
    for index, user in enumerate(users):
        if user.id == user_id:
            users[index] = updated_user
            return updated_user
    raise HTTPException(status_code=404, detail="User not found")


@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return {"message": "Deleted Successfully"}
    raise HTTPException(status_code=404, detail="User not found")