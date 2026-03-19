import os
from fastapi import APIRouter, Request

router = APIRouter()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")


@router.get("/webhook")
async def verify(request: Request):
    params = request.query_params

    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    print("DEBUG:", mode, token, challenge)

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return int(challenge)

    return {"error": "Verification failed"}


@router.post("/webhook")
async def receive_message(request: Request):
    body = await request.json()
    print("📩 Mensagem recebida:", body)

    return {"status": "ok"}