from fastapi import FastAPI
from routers.images import router as images_router
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

app.include_router(images_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Azure Blob Image API!"}