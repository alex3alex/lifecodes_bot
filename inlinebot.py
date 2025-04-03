import os
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

from telegram import Bot

TOKEN = os.environ.get("BOT_TOKEN")
APP_NAME = os.environ.get("APP_NAME")

app = FastAPI()

class TelegramWebhook(BaseModel):
    '''
    Telegram Webhook Model using Pydantic for request body validation
    '''
    update_id: int
    message: Optional[dict]
    edited_message: Optional[dict]
    channel_post: Optional[dict]
    edited_channel_post: Optional[dict]
    inline_query: Optional[dict]
    chosen_inline_result: Optional[dict]
    callback_query: Optional[dict]
    shipping_query: Optional[dict]
    pre_checkout_query: Optional[dict]
    poll: Optional[dict]
    poll_answer: Optional[dict]

def send_message(chat_id, text):
    """
    Helper function to send a message using Telegram Bot API.
    """
    bot = Bot(token=TOKEN)
    bot.send_message(chat_id=chat_id, text=text)

@app.post("/webhook")
def webhook(webhook_data: TelegramWebhook):
    '''
    Telegram Webhook
    '''
    # Метод 1 (закомментирован)
    # bot = Bot(token=TOKEN)
    # update = Update.de_json(webhook_data.__dict__, bot)  # convert the Telegram Webhook class to dictionary using __dict__ dunder method
    # dispatcher = Dispatcher(bot, None, workers=4)
    # register_handlers(dispatcher)
    # dispatcher.process_update(update)

    # Метод 2 (используется)
    if webhook_data.message:
        if webhook_data.message.get("text") == '/start':
            chat_id = webhook_data.message["chat"]["id"]
            send_message(chat_id, "Hello World")

    return {"message": "ok"}

@app.get("/")
def index():
    return {"message": "Hello World"}
