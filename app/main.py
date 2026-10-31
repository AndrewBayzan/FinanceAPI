from fastapi import FastAPI

from app.routes.users import router as users_router

app = FastAPI()

app.include_router(users_router)

@app.get("/home")
def home():
    return "Hello World"