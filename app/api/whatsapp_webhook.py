import os
import requests
from fastapi import APIRouter, Request

router = APIRouter()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")

processed_messages = set()


def send_whatsapp_message(to, text):
    url = f"https://graph.facebook.com/v22.0/{os.getenv('PHONE_NUMBER_ID')}/messages"

    headers = {
        "Authorization": f"Bearer {os.getenv('META_WHATSAPP_TOKEN')}",
        "Content-Type": "application/json"
    }

    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text}
    }

    response = requests.post(url, headers=headers, json=data)
    print("📤 Enviado:", response.text)


# ✅ GET (OBRIGATÓRIO)
@router.get("/webhook")
async def verify(request: Request):
    params = request.query_params

    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return int(challenge)

    return {"error": "Verification failed"}


# ✅ POST (MENSAGENS)
@router.post("/webhook")
async def receive_message(request: Request):
    body = await request.json()
    print("📩 Mensagem recebida:", body)

    try:
        message = body["entry"][0]["changes"][0]["value"]["messages"][0]
        message_id = message["id"]

        # evita duplicação
        if message_id in processed_messages:
            return {"status": "duplicated"}

        processed_messages.add(message_id)

        from_number = message["from"]
        text = message["text"]["body"]

        print(f"👤 Cliente disse: {text}")

        send_whatsapp_message(
            from_number,
            "Olá 👋 Bem-vindo!\nVeja nosso sites abaixo:"
            "catálogo menina lancamento: https://calpi.com"
            "catalogo lauban para pedir pix -- Junlei - famoso - Larissa - xaltin"
            " quer tonchi? xalpai.com"


        )

    except Exception as e:
        print("Erro:", e)

    return {"status": "ok"}