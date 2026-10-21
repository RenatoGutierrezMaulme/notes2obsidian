from pathlib import Path
from enum import Enum
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT = Path(__file__).resolve().parents[2]

# str -> create a "str" object
class StandardFormats(str, Enum):
    CSV = "csv"
    JSON = "json"
    MARKDOWN = "markdown"
    HTML = "html"

class Settings(BaseSettings):

    # ----------- Input ----------------------
    model_config = SettingsConfigDict(
        env_file = ROOT / ".env",
        env_file_encoding = "utf-8",
        extra = "ignore",
    )

    telegram_bot_token    : SecretStr
    telegram_bot_username : SecretStr

    def telegram_bot_token(self):
        return self.telegram_bot_token
    def telegram_bot_username(self):
        return self.telegram_bot_username

    use_llm : bool = False

    # ----------- Output ----------------------
    output_format: StandardFormats = StandardFormats.MARKDOWN
    output_path: Path = ROOT / "output"


#print(Settings().telegram_bot_token)





