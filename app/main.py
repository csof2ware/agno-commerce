from fastapi import FastAPI
from app.api import whatsapp_webhook

app = FastAPI()

@app.get("/")
def home():
    return {"status": "AGNO Commerce Running"}

app.include_router(whatsapp_webhook.router)