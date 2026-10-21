"""
Help command for RenatoNotesBot
"""
from telegram import Update

COMMANDS_DESCRIPTIONS = {
    "/help": {"description": "General use of the bot", "args": []},
    "/image2md": {"description" : "Upload one or more images and produces a markdown file", "args": ["fast", "llm"]},
    "/pdf2md": {"description": "Upload PDF and produces a markdown file", "args": ["fast", "llm"]},
}

def available_commands(commands: dict) -> str:

    lines = []
    for name, info in commands.items():
        lines.append(f"{name}: {info['description']}")
        if info["args"]:
            lines.append(f"     Args: {info['args']}")
        else:
            lines.append(f"     Args: None")

    output = "\n".join(lines)


    return (f"To call a command, type /command [arguments].\n"
            f"For example, if you want to pass from a PDF file to a Markdown file with LLM tools type /pdf2md llm.\n"
            f"List of available commands:\n\n"
            f"{output}")

print(available_commands(COMMANDS_DESCRIPTIONS))