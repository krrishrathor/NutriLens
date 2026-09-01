from fastapi import FastAPI
from app.api.analyze import router as router

app = FastAPI(
    title = "NutriLens API",
    version = "1.0.0"
)

app.include_router(router)

@app.get("/")
def home():
    return {"message": "NutriLens API is running"}