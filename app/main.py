from fastapi import FastAPI

from app.routes.users import router as users_router
from app.routes.auth import router as auth_router

app = FastAPI()

app.include_router(users_router)
app.include_router(auth_router)

@app.get("/home")
def home():
    return "Hello World"