from dataclasses import dataclass

@dataclass(frozen=True)
class BotCommand:
    name: str
    description: str
    args: tuple[str, ...] = ()

COMMANDS = {
    c.name: c for c in (
        BotCommand("help", "General use of the bot"),
        BotCommand("image2md", "Upload one or more images and produces a markdown file", ("fast", "llm")),
        BotCommand("pdf2md", "Upload PDF and produces a markdown file", ("fast", "llm")),
    )
}

