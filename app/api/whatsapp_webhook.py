from fastapi import APIRouter, Request

router = APIRouter()

VERIFY_TOKEN = "meu_token_verificacao"

@router.get("/webhook")
async def verify(request: Request):
    params = request.query_params

    if (
        params.get("hub.mode") == "subscribe"
        and params.get("hub.verify_token") == VERIFY_TOKEN
    ):
        return int(params.get("hub.challenge"))

    return {"error": "Verification failed"}


@router.post("/webhook")
async def receive_message(request: Request):
    body = await request.json()
    print("Mensagem recebida:", body)

    return {"status": "ok"}