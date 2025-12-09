from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()

# Citește tokenul din variabila de mediu
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

def send_message(chat_id: int, text: str):
    """Trimite mesaj înapoi către Telegram chat."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    response = requests.post(url, json={"chat_id": chat_id, "text": text})
    print("Telegram response:", response.text)  # debug
    return response

@app.get("/")
def home():
    return {"status": "Telegram bot backend is running"}

@app.post("/")
async def webhook(req: Request):
    data = await req.json()
    print("Webhook data:", data)  # debug

    message = data.get("message")
    if not message:
        return {"ok": True}

    chat_id = message["chat"]["id"]
    user_text = message.get("text", "<no text>")

    reply = f"Am primit mesajul tău: {user_text}"
    send_message(chat_id, reply)

    return {"ok": True}
