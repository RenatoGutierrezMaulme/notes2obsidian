import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from config import Settings

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hi! This is my personal bot for notes managing. Paste a photo, pdf, audio or whatever you want"
             " in the chat and specify what do you want to do with it. For now, not LLM is reading your inputs"
             " so you have to use commands!. Use /commands to see the list of available commands",
    )

# available commands
async def commands(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="This is the command list")

# "not found command" handler
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="This command do not exists")

def main():
    application = ApplicationBuilder().token(Settings().telegram_bot_token.get_secret_value()).build()

    start_handler = CommandHandler("start", start)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    args_handler = CommandHandler("commands", commands)

    application.add_handler(start_handler)
    application.add_handler(args_handler)
    application.add_handler(unknown_handler)

    application.run_polling()

if __name__ == "__main__":
    main()

