import logging
import os
from html import escape
from uuid import uuid4

from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes, InlineQueryHandler
from flask import Flask, request

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

TOKEN = os.environ.get("BOT_TOKEN")

if not TOKEN:
    print("BOT_TOKEN is not set")
    exit(1)

APP_NAME = os.environ.get("APP_NAME")

if not APP_NAME:
    print("APP_NAME is not set")
    exit(1)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hi! Use inline mode to get caps, bold or italic versions of your text!')

async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    if not query:
        return

    results = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),
            title='Bold',
            input_message_content=InputTextMessageContent(
                f'<b>{escape(query)}</b>', parse_mode=ParseMode.HTML
            ),
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),
            title='Italic',
            input_message_content=InputTextMessageContent(
                f'<i>{escape(query)}</i>', parse_mode=ParseMode.HTML
            ),
        ),
    ]
    await update.inline_query.answer(results)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f'Update {update} caused error {context.error}')

application = Application.builder().token(TOKEN).build()
application.add_handler(CommandHandler('start', start))
application.add_handler(InlineQueryHandler(inline_query))
application.add_error_handler(error_handler)

@app.route('/' + TOKEN, methods=['POST'])
async def webhook():
    try:
        data = request.get_json(force=True)
        if not data:
            return 'Invalid JSON', 400
        update = Update.de_json(data, application.bot)
        await application.process_update(update)
        return 'ok'
    except Exception as e:
        logger.error(f'Error processing update: {e}')
        return 'Error', 500

@app.route('/set_webhook', methods=['GET', 'POST'])
async def set_webhook():
    webhook_url = f"https://{APP_NAME}.vercel.app/{TOKEN}"
    try:
        await application.bot.set_webhook(webhook_url)
        return f"Webhook set to {webhook_url}"
    except Exception as e:
        return f"Error setting webhook: {e}"

@app.route('/')
def index():
    return "<h1>Server is running</h1>"

if __name__ == '__main__':
    app.run(threaded=True)
