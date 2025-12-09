# main.py
from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text})

@app.post("/")
async def webhook(req: Request):
    data = await req.json()
    message = data.get("message") or data.get("edited_message")
    if not message:
        return {"ok": True}

    chat_id = message["chat"]["id"]
    user_text = message.get("text", "")

    # fallback simplu dacă nu e text
    if not user_text:
        send_message(chat_id, "Trimite un mesaj text.")
        return {"ok": True}

    ai_response = call_ai(user_text)
    send_message(chat_id, ai_response)
    return {"ok": True}

def call_ai(prompt):
    # Exemplu minimal cu OpenAI (chat)
    import openai
    openai.api_key = OPENAI_API_KEY
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Ești un agent conversațional util, clar și concis."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
    )
    return response.choices[0].message["content"]
