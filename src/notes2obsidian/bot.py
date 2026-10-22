import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from notes2obsidian.config import Settings
from notes2obsidian.commands import help

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hi! This is my personal bot for notes managing. Paste a photo, pdf, audio or whatever you want"
             " in the chat and specify what do you want to do with it. For now, not LLM is reading your inputs"
             " so you have to use commands!. \nUse /help to see the list of available commands and how to use it",
    )

# help command handler
async def help_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=help.available_commands())

# "not found command" handler
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="This command do not exists")

def main():
    application = ApplicationBuilder().token(Settings().telegram_bot_token.get_secret_value()).build()

    start_handler = CommandHandler("start", start)
    help_handler = CommandHandler("help", help_bot)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)

    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(unknown_handler)

    application.run_polling()

if __name__ == "__main__":
    main()

