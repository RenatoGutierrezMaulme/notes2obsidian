from config import StandardFormats
import logging
import asyncio
import telegram

from config import Settings

# Implementation of the bot (for now is a linked with Telegram)

FORMAT_ALIASES = {
    "markdown": StandardFormats.MARKDOWN, "md" : StandardFormats.MARKDOWN,
    "json" : StandardFormats.JSON,
}

async def main():
    bot = telegram.Bot(Settings().telegram_bot_token.get_secret_value())
    async with bot:
        print(await bot.get_me())


if __name__ == "__main__":
    asyncio.run(main())