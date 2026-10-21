from config import StandardFormats
import logging
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from config import Settings

"""
Telegram Bot that takes the user file input to a structured format
Author: Renato Gutiérrez
"""

FORMAT_ALIASES = {
    "markdown": StandardFormats.MARKDOWN, "md" : StandardFormats.MARKDOWN,
    "json" : StandardFormats.JSON,
}

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="This is the bot for files processing into structured format (markdown, json, etc.)",
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

def main():
    application = ApplicationBuilder().token(Settings().telegram_bot_token.get_secret_value()).build()

    start_handler = CommandHandler("start", start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)

    application.add_handler(start_handler)
    application.add_handler(echo_handler)

    application.run_polling()

if __name__ == "__main__":
    main()

