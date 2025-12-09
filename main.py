from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()

TELEGRAM_TOKEN = os.getenv("8544231370:AAH1hR98A_NqzEnWH4nIL2yfzHorFsVNGzQ")

def send_message(chat_id: int, text: str):
    """Trimite mesaj înapoi către Telegram chat."""
    url = f"https://api.telegram.org/bot{8544231370:AAH1hR98A_NqzEnWH4nIL2yfzHorFsVNGzQ}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text})

@app.get("/")
def home():
    """Endpoint simplu pentru test în browser."""
    return {"status": "Telegram bot backend is running"}

@app.post("/")
async def webhook(req: Request):
    """Endpoint webhook pentru Telegram."""
    data = await req.json()
    message = data.get("message")
    if not message:
        return {"ok": True}

    chat_id = message["chat"]["id"]
    user_text = message.get("text", "")

    # Răspuns simplu, fără AI
    reply = f"Am primit mesajul tău: {user_text}"
    send_message(chat_id, reply)

    return {"ok": True}
